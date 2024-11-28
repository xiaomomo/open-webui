import os
import sys
import requests
from urllib.parse import urlparse
import json
import asyncio
import random
import aiohttp
import aiofiles

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../../../'))
sys.path.append(project_root)

# Now import the modules
from open_webui.apps.englishlesson.chineselesson.workflows.chineselesson.screenplay_workflow import ScreenplayWorkflow
from open_webui.apps.englishlesson.chineselesson.workflows.chineselesson.screenplay_overview_image_workflow import ScreenplayImageWorkflow
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessons


def saveImageToStatic(screenplayImageUrl):
    # Define the static folder path
    static_folder = "/Users/liuqingjie/code/ai-tts/open-webui/static/static/screenplay_resource/"
    
    # Create the directory if it doesn't exist
    os.makedirs(static_folder, exist_ok=True)
    
    try:
        # Get the filename from the URL
        parsed_url = urlparse(screenplayImageUrl)
        filename = os.path.basename(parsed_url.path)
        
        # If filename is empty or has no extension, generate a default one
        if not filename or '.' not in filename:
            filename = f"screenplay_{hash(screenplayImageUrl)}.png"
        
        # Full path where the image will be saved
        save_path = os.path.join(static_folder, filename)
        
        # Download and save the image
        response = requests.get(screenplayImageUrl, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        # Return the relative path that can be used in the frontend
        return f"/static/screenplay_resource/{filename}"
    
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None

# 定义配对的可选值
VOICE_OPTIONS = {
    'host': {
        'refer_wav': 'output/slicer_opt/blippi_v3.mp3_0004445440_0004588480.wav',
        'prompt_text': 'Wait! Look at this! It\'s a beautiful couch!',
        'speaker_name': 'default'
    },
    'character': {
        'refer_wav': 'output/data/littlepony/slicer_opt/littlepony5minter.m4a_0007617920_0007816960.wav',
        'prompt_text': 'I don\'t want to go either. Nope, I\'ve made up my mind. Spike, you can send the letter now. It\'s okay, girls.',
        'speaker_name': 'littleponyv2'
    }
}

# 添加这些常量定义
base_url = "http://127.0.0.1:9880"  # 替换为实际的 TTS 服务 URL
static_audio_folder = "/Users/liuqingjie/code/ai-tts/open-webui/static/static/screenplay_audio/"

async def generate_audio(text, filename, voice_type='host', max_retries=3):
    # 确保音频目录存在
    os.makedirs(static_audio_folder, exist_ok=True)
    
    voice_config = VOICE_OPTIONS[voice_type]
    params = {
        'refer_wav_path': voice_config['refer_wav'],
        'prompt_text': voice_config['prompt_text'],
        'prompt_language': 'en',
        'text': text,
        'text_language': 'zh',
        'speaker_name': voice_config['speaker_name']
    }
    
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params) as response:
                    if response.status != 200:
                        print(f"Error response from TTS service: {response.status}")
                        print(f"Response text: {await response.text()}")
                        if attempt < max_retries - 1:
                            print(f"Retrying... Attempt {attempt + 2}/{max_retries}")
                            await asyncio.sleep(1)  # 等待1秒后重试
                            continue
                        return None
                    
                    # Handle streaming response
                    chunks = []
                    async for chunk in response.content.iter_any():
                        chunks.append(chunk)
                    content = b''.join(chunks)
            
            audio_path = os.path.join(static_audio_folder, filename)
            async with aiofiles.open(audio_path, 'wb') as f:
                await f.write(content)
            
            return f"/static/screenplay_audio/{filename}"
            
        except (aiohttp.ClientError, TransferEncodingError) as e:
            print(f"Network error while generating audio for {filename}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying... Attempt {attempt + 2}/{max_retries}")
                await asyncio.sleep(1)  # 等待1秒后重试
                continue
            return None
        except Exception as e:
            print(f"Unexpected error generating audio for {filename}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying... Attempt {attempt + 2}/{max_retries}")
                await asyncio.sleep(1)  # 等待1秒后重试
                continue
            return None
    
    return None


async def generate_all_audio(screenplay):
    tasks = []
    
    # 生成8位随机字符串的辅助函数
    def get_random_string():
        return ''.join(random.choices('0123456789abcdef', k=8))
    
    # 场景描述音频
    if 'screenContent' in screenplay:
        task = generate_audio(
            screenplay['screenContent'],
            f"screen_content_{hash(screenplay['screenContent'])}_{get_random_string()}.wav"
        )
        tasks.append(('screenContent', task))

    # 角色对话音频 - 保持顺序
    if 'charactersBehavior' in screenplay:
        for idx, character in enumerate(screenplay['charactersBehavior']):
            if 'behaviorContent' in character:
                task = generate_audio(
                    character['behaviorContent'],
                    f"character_{character['charactersName']}_{idx}_{hash(character['behaviorContent'])}_{get_random_string()}.wav",
                    voice_type='character'
                )
                tasks.append((f"character_{idx}", task))

    # 问题音频
    if 'whatNextMainPlayerShouldDo' in screenplay:
        question_section = screenplay['whatNextMainPlayerShouldDo']
        
        if 'question' in question_section:
            task = generate_audio(
                question_section['question'],
                f"question_{hash(question_section['question'])}_{get_random_string()}.wav"
            )
            tasks.append(('question', task))
        
        if 'playerChoice' in question_section:
            for choice in question_section['playerChoice']:
                if 'content' in choice:
                    task = generate_audio(
                        choice['option']+"-"+choice['content'],
                        f"option_{choice['option']}_{hash(choice['content'])}_{get_random_string()}.wav"
                    )
                    tasks.append((f"option_{choice['option']}", task))

    # 并行执行所有任务
    results = await asyncio.gather(*[task[1] for task in tasks])
    
    # 将结果更新到 screenplay
    for (task_key, _), result in zip(tasks, results):
        if task_key == 'screenContent':
            screenplay['screenContentAudio'] = result
        elif task_key.startswith('character_'):
            # Get the index from the task_key
            idx = int(task_key.replace('character_', ''))
            screenplay['charactersBehavior'][idx]['behaviorContentAudio'] = result
        elif task_key == 'question':
            screenplay['whatNextMainPlayerShouldDo']['questionAudio'] = result
        elif task_key.startswith('option_'):
            option_num = task_key.replace('option_', '')
            for choice in screenplay['whatNextMainPlayerShouldDo']['playerChoice']:
                if choice['option'] == option_num:
                    choice['optionAudio'] = result

    return screenplay


async def save_unit(item):

    # 调用工作流结构化screenplay
    w = ScreenplayWorkflow(timeout=600, verbose=False)
    print(f"workflow start with content:{item}")
    screenplay = await w.run(origin_content=item)

    # 调用工作流生成图片
    w = ScreenplayImageWorkflow(timeout=600, verbose=False)
    screenplayImage = await w.run(origin_content=item)
    # save it to static folder
    screenplayImagePath = saveImageToStatic(screenplayImage)
    print(f"workflow generate question_json:{screenplayImage}")
    screenplay_dict = json.loads(screenplay) if isinstance(screenplay, str) else screenplay
    # save item to sqlite
    fredisaLesson = FredisaLessonForm(
        unit=screenplay_dict['title'],
        subject="Chinese",
        content=item,
        lesson_json=screenplay,
        question_json="",
        lesson_img=screenplayImagePath
    )
    
    # 首屏的音频生成
    await generate_all_audio(screenplay_dict['scenes'][0])
    # 这里又用更新后的 screenplay_dict 重新序列化
    fredisaLesson.lesson_json = json.dumps(screenplay_dict, ensure_ascii=False)
    
    print(f"workflow generate question_json:{fredisaLesson.lesson_json}")

    # lesson = FredisaLessons.insert_new_lesson(fredisaLesson)
    # return lesson

async def process_all_stories():
    try:
        # Read the JSON file
        with open('./grimm_stories_v2.json', 'r', encoding='utf-8') as file:
            stories = json.load(file)

        # Process each story
        for index, story in enumerate(stories):
            print(f"Processing story {index + 1}/{len(stories)}")
            try:
                await save_unit(story['content'])
                print(f"Successfully processed story {index + 1}")
            except Exception as e:
                print(f"Error processing story {index + 1}: {str(e)}")
                continue

        print("All stories have been processed")

    except FileNotFoundError:
        print("Error: grimm_stories_v2.json file not found in current directory")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in grimm_stories_v2.json")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

async def test_save_unit():
    # Test data
    test_item = """
   
{
    "title": "小红帽的冒险",
    "difficulty": "Intermediate",
    "screenplayIntro":"这是一个关于小红帽和妈妈的冒险故事。你准备好开始了吗？",
    "characters": [
        {
            "name": "猎人",
            "role": "英雄角色",
            "background": "森林里的猎人，勇敢且机智。",
            "personality": "勇敢、正义感强",
            "languageLevel": "高级",
            "isMainPlayer": false
        },
        {
            "name": "奶奶",
            "role": "支持角色",
            "background": "住在森林深处的老奶奶，身体虚弱。",
            "personality": "慈祥、智慧",
            "languageLevel": "中级",
            "isMainPlayer": false
        }
    ],
    "scenes": [
        {
            "location": "小红帽家的厨房",
            "timeOfDay": "早晨",
            "screenContent": "清晨，阳光透过窗户洒在厨房里。妈妈正在准备一块蛋糕和一瓶葡萄酒，打算让小红帽送给生病的奶奶。厨房里弥漫着新鲜烘焙的香气。",
            "charactersBehavior": [
                {
                    "charactersName": "妈妈",
                    "behaviorType": "speaking",
                    "behaviorContent": "来，小红帽，这里有一块蛋糕和一瓶葡萄酒，快给奶奶送去。奶奶生病了，身子很虚弱，吃了这些就会好一些的。趁着现在天还没有热，赶紧动身吧。在路上要好好走，不要跑，也不要离开大路，否则你会摔跤的，那样奶奶就什么也吃不上了。到奶奶家的时候，别忘了说'早上好'，也不要一进屋就东瞧西瞅。"
                },
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "我会小心的。"
                },
                {
                    "charactersName": "妈妈",
                    "behaviorType": "speaking",
                    "behaviorContent": "123456"
                },
                {
                    "charactersName": "妈妈",
                    "behaviorType": "speaking",
                    "behaviorContent": "789"
                },
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "101112。"
                }
                
            ],
            "whatNextMainPlayerShouldDo": {
                "question": "你准备好出发了吗？",
                "answerType": "choose",
                "playerChoice": [
                    {
                        "option": "A",
                        "content": "是的，我已经准备好了。"
                    },
                    {
                        "option": "B",
                        "content": "我还需要再检查一下东西。"
                    }
                ]
            }
        },
        {
            "playerChoiceEvaluate": "如果选择A，小红帽会直接出发；如果选择B，小红帽会再检查一遍东西，但最终还会出发。",
            "location": "森林入口",
            "timeOfDay": "上午",
            "screenContent": "小红帽提着篮子走进了森林。阳光透过树叶洒在地上，小鸟在枝头歌唱。突然，一只狼出现在她面前。",
            "charactersBehavior": [
                {
                    "charactersName": "狼",
                    "behaviorType": "speaking",
                    "behaviorContent": "你好，小红帽。这么早要到哪里去呀？"
                },
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "我要到奶奶家去。"
                },
                {
                    "charactersName": "狼",
                    "behaviorType": "speaking",
                    "behaviorContent": "你那围裙下面有什么呀？"
                },
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "蛋糕和葡萄酒。昨天我们家烤了一些蛋糕，可怜的奶奶了病，要吃一些好东西才能恢复过来。"
                }
            ],
            "whatNextMainPlayerShouldDo": {
                "question": "你会告诉狼奶奶住在哪里吗？",
                "answerType": "choose",
                "playerChoice": [
                    {
                        "option": "A",
                        "content": "不，我不告诉你。"
                    },
                    {
                        "option": "B",
                        "content": "进了林子还有一段路呢。她的房子就在三棵大橡树下，低处围着核桃树篱笆。你一定知道的。"
                    }
                ]
            }
        },
        {
            "playerChoiceEvaluate": "如果选择A，狼会假装友善并继续跟随小红帽；如果选择B，狼会直接去找奶奶。",
            "location": "森林深处",
            "timeOfDay": "中午",
            "screenContent": "小红帽被周围的美景吸引，开始采花。她越走越深，忘记了时间。与此同，狼找到了奶奶的家，并吞下了奶奶。",
            "charactersBehavior": [
                {
                    "charactersName": "小红帽",
                    "behaviorType": "thinking",
                    "behaviorContent": "也许我该摘一把鲜花给奶奶，让她高兴高兴。现在天色还早，我不会去迟的。"
                },
                {
                    "charactersName": "狼",
                    "behaviorType": "motion",
                    "behaviorContent": "狼冲到奶奶的床前，把奶奶吞进了肚子。然后她穿上奶奶的衣服，戴上她的帽子，躺在床上，拉上了帘子。"
                }
            ],
            "whatNextMainPlayerShouldDo": {
                "question": "你发现时间已经很晚了吗？",
                "answerType": "choose",
                "playerChoice": [
                    {
                        "option": "A",
                        "content": "是的，我应该赶快去奶奶家。"
                    },
                    {
                        "option": "B",
                        "content": "再采一些花吧，反正已经晚了。"
                    }
                ]
            }
        }
    ]
}
    
    """
    
    try:
        # Test the save_unit function
        result = await save_unit(test_item)
        
        # Verify the result
        assert result is not None, "save_unit should return a lesson"
        print("✅ Test passed: save_unit returned a lesson")
        
        # Verify audio generation
        screenplay_dict = json.loads(result.lesson_json)
        first_scene = screenplay_dict['scenes'][0]
        
        assert 'screenContentAudio' in first_scene, "Screen content audio should be generated"
        assert first_scene['charactersBehavior'][0].get('behaviorContentAudio'), "Character audio should be generated"
        assert first_scene['whatNextMainPlayerShouldDo'].get('questionAudio'), "Question audio should be generated"
        
        print("✅ Test passed: All audio files were generated")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

# if __name__ == "__main__":
#     asyncio.run(test_save_unit())

if __name__ == "__main__":
    asyncio.run(process_all_stories())

