from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)
from dashscope import Generation, ImageSynthesis
import json
from prompts import *
import logging
from typing import Union
import os
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests

# Create logger instance
logger = logging.getLogger(__name__)

# workflow step:
#     1. start
#     2. split screen of screenplay
#     3. generate core info
#     4. generate image by core info
#     5. finish

class SplitScreenplayEvent(Event):
    screenplay: str

class GenerateCoreInfoEvent(Event):
    scenes: list[dict]

class GenerateImageEvent(Event):
    core_info: dict

class CollectImagesEvent(Event):
    screenplay: str
    image_result: dict

class ScreenplayImageWorkflow(Workflow):
    @step
    async def step_start(self, ctx: Context, ev: StartEvent) -> SplitScreenplayEvent:
        print(f"Starting workflow with content: {ev.origin_content}")
        # Store screenplay in context
        await ctx.set("screenplay", ev.origin_content)
        return SplitScreenplayEvent(screenplay=ev.origin_content)

    @step
    async def step_split_screenplay(self, ctx: Context, ev: SplitScreenplayEvent) -> GenerateCoreInfoEvent:
        print("Splitting screenplay into scenes")
        try:
            screenplayJson = json.loads(ev.screenplay)
            scenes = screenplayJson["scenes"]
            # Send multiple events for parallel processing
            for scene in scenes:
                ctx.send_event(GenerateCoreInfoEvent(scenes=[scene]))
        except Exception as e:
            logger.error("Failed to split screenplay: %s", str(e))
            raise

    @step(num_workers=4)  # Process up to 4 scenes concurrently
    async def step_generate_core_info(self, ctx: Context, ev: GenerateCoreInfoEvent) -> GenerateImageEvent:
        scene = ev.scenes[0]  # Since we're now processing one scene at a time
        print(f"Generating core information for scene {scene['sceneNumber']}")
        try:
            prompt = prompt_generate_core_info.format(scene=scene)
            response = Generation.call(
                model='qwen-max',
                messages=[{'role': 'user', 'content': prompt}]
            )
            core_info = response.output.text
            print(f"Generated core information: {core_info}")
            core_info_dict = {'sceneNumber': scene['sceneNumber'], 'core_info': core_info}
            ctx.send_event(GenerateImageEvent(core_info=core_info_dict))
        except Exception as e:
            logger.error(f"Failed to generate core info for scene: {str(e)}")
            raise

    @step(num_workers=4)  # Process up to 4 images concurrently
    async def step_generate_images(self, ctx: Context, ev: GenerateImageEvent) -> CollectImagesEvent:
        print(f"Generating image for scene {ev.core_info}")
        try:
            scene_num = ev.core_info['sceneNumber']
            core_info = ev.core_info['core_info']
            
            # Call ImageSynthesis API
            response = ImageSynthesis.call(
                model=ImageSynthesis.Models.wanx_v1,
                prompt=core_info,
                n=1,
                size='1024*1024'
            )

            image_result = None
            if response.status_code == HTTPStatus.OK:
                # Get the first image URL from results
                if response.output.results:
                    image_url = response.output.results[0].url
                    image_result = image_url
            else:
                logger.error('Image generation failed, status_code: %s, code: %s, message: %s',
                          response.status_code, response.code, response.message)
                raise Exception(f"Image generation failed: {response.message}")

            # Get screenplay from context
            screenplay = await ctx.get("screenplay")
            return CollectImagesEvent(
                screenplay=screenplay,
                image_result={scene_num: image_result}
            )
        except Exception as e:
            logger.error(f"Failed to generate image: {str(e)}")
            raise

    @step
    async def step_collect_results(self, ctx: Context, ev: CollectImagesEvent) -> StopEvent:
        # Get screenplay from context - add await here
        screenplay = json.loads(await ctx.get("screenplay"))
        result = ctx.collect_events(ev, [CollectImagesEvent] * len(screenplay["scenes"]))
        if result is None:
            return None

        # Combine all results into a single dictionary
        combined_results = {}
        for event in result:
            combined_results.update(event.image_result)
        
        return StopEvent(result={"images": combined_results})

async def main():
    print("Starting main workflow execution")
    # Test content
    test_content = """
{
    "title": "小红帽的中文冒险",
    "difficulty": "Beginner",
    "mainCharacters": [
        {
            "name": "小红帽",
            "role": "主角",
            "background": "一个可爱的小姑娘，总是戴着奶奶送给她的红色丝绒帽子。她天真无邪，好奇心强。",
            "personality": "善良、好奇、有点儿天真",
            "languageLevel": "初级"
        },
        {
            "name": "妈妈",
            "role": "支持角色",
            "background": "小红帽的母亲，非常关心女儿的安全和教育。",
            "personality": "慈爱、谨慎",
            "languageLevel": "中级"
        },
        {
            "name": "奶",
            "role": "支持角色",
            "background": "住在森林里的老奶奶，非常疼爱小红帽。",
            "personality": "慈祥、智慧",
            "languageLevel": "高级"
        },
        {
            "name": "狼",
            "role": "反派",
            "background": "狡猾的狼，试图欺骗小红帽。",
            "personality": "狡猾、贪婪",
            "languageLevel": "高级"
        }
    ],
    "scenes": [
        {
            "sceneNumber": 1,
            "location": "小红帽家的厨房",
            "timeOfDay": "早上",
            "screenContent": "阳光透过窗户洒进厨房，妈妈正在准备蛋糕和葡萄酒。小红帽坐在餐桌旁，认真听着妈妈的叮嘱。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "妈妈",
                        "chinese": "来，小红帽，这里有一块蛋糕和一瓶葡萄酒，快给奶奶送去。奶奶生病了，身子很虚弱，吃了这些就会好一些的。"
                    },
                    {
                        "character": "小红帽",
                        "chinese": "我会小心的。"
                    }
                ],
                "actions": "妈妈把蛋糕和葡萄酒递给小红帽，小红帽接过东西，向妈妈保证会注意安全。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "chinese": "直接去奶奶家",
                    "consequence": "小红帽直接前往奶奶家，路上没有遇到狼。"
                },
                {
                    "option": "B",
                    "chinese": "先在花园里采花",
                    "consequence": "小红帽决定去花园采花，结果遇到了狼。"
                }
            ]
        },
        {
            "sceneNumber": 2,
            "location": "森林小路",
            "timeOfDay": "上午",
            "screenContent": "小红帽走在森林小路上，四周是茂密的树木和美丽的花朵。阳光透过树叶洒在地上，形成斑驳的光影。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "狼",
                        "chinese": "你好，小红帽，这么早要到哪里去呀？"
                    },
                    {
                        "character": "小红帽",
                        "chinese": "我要到奶奶去。"
                    }
                ],
                "actions": "狼装作友善的样子，与小红帽交谈。红帽天真地回答狼的问题。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "chinese": "告诉狼奶奶的住址",
                    "consequence": "小红帽告诉狼奶奶的住址，狼计划直接去找奶奶。"
                },
                {
                    "option": "B",
                    "chinese": "保持警惕，不透露信息",
                    "consequence": "小红帽保持警惕，没有告诉狼奶奶的具体住址。"
                }
            ]
        },
        {
            "sceneNumber": 3,
            "location": "奶奶的房子",
            "timeOfDay": "中午",
            "screenContent": "奶奶的房子坐落在三棵大橡树下，周围是核桃树篱笆。房门敞开着，显得有些奇怪。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "小红帽",
                        "chinese": "早上好！"
                    },
                    {
                        "character": "狼（假扮奶奶）",
                        "chinese": "哎，奶奶，你的耳朵怎么这样大呀？"
                    },
                    {
                        "character": "小红帽",
                        "chinese": "为了更好地听你说话呀，乖乖。"
                    }
                ],
                "actions": "小红帽走进房子，发现奶奶躺在床上，但感觉有些不对劲。她开始询问奶奶的变化。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "chinese": "继续问问题",
                    "consequence": "小红帽继续提问，最终被狼吞掉。"
                },
                {
                    "option": "B",
                    "chinese": "察觉危险，逃跑",
                    "consequence": "小红帽察觉到危险，赶紧逃跑并寻求帮助。"
                }
            ]
        },
        {
            "sceneNumber": 4,
            "location": "猎人的小屋",
            "timeOfDay": "下午",
            "screenContent": "猎人正巧路过奶奶的房子，听到里面的动静后进去查看。他发现了狼并救出了小红帽和奶奶。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "猎人",
                        "chinese": "这老太太鼾打得好响啊！我要进去看看她是不是出什么事了。"
                    },
                    {
                        "character": "小红帽",
                        "chinese": "真把我吓坏了！狼肚子里黑漆漆的。"
                    }
                ],
                "actions": "猎人用剪刀剪开狼的肚子，救出了小红帽和奶奶。小红帽感激不已。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "chinese": "感谢猎人",
                    "consequence": "小红帽真诚地感谢猎人，建立了友谊。"
                },
                {
                    "option": "B",
                    "chinese": "感到害怕，哭泣",
                    "consequence": "小红帽感到害怕，哭了起来，猎人安慰她。"
                }
            ]
        },
        {
            "sceneNumber": 5,
            "location": "奶奶的房子",
            "timeOfDay": "傍晚",
            "screenContent": "奶奶吃了小红帽带来的蛋糕和葡萄酒，精神好多了。小红帽和奶奶一起回忆今天的经历，并决定以后更加小心。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "奶奶",
                        "chinese": "我们把门关紧，不让它进来。"
                    },
                    {
                        "character": "小红帽",
                        "chinese": "要是妈妈不允许，我一辈子也不独自离开大路，跑进森林了。"
                    }
                ],
                "actions": "小红帽和奶奶一起加固房子的防御措施，确保不再有危险。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "chinese": "提议下次送蛋糕时更小心",
                    "consequence": "小红帽提议下次送蛋糕时更加小心，奶奶表示赞同。"
                },
                {
                    "option": "B",
                    "chinese": "决定再也不独自出门",
                    "consequence": "小红帽决定再也不独自出门，奶奶安慰她。"
                }
            ]
        }
    ],
    "storyProgression": {
        "beginning": "小红帽接受妈妈的务，准备去奶奶家送蛋糕和葡萄酒。",
        "middle": "小红帽在路上遇到狼，被骗去了奶奶家。狼吃掉了奶奶并假扮成奶奶等待小红帽。小红帽察觉到危险，但最终还是被狼吞掉。猎人及时赶到，救出了小红帽和奶奶。",
        "end": "小红帽和奶奶平安归来，决定以后更加小心。小红帽学会了警惕和自我保护的重要性。"
    },
    "learning": {
        "keyVocabulary": [
            {
                "chinese": "蛋糕",
                "pinyin": "dàngāo",
                "usage": "妈妈给小红帽一块蛋糕。"
            },
            {
                "chinese": "葡萄酒",
                "pinyin": "pútáojiǔ",
                "usage": "妈妈给小红帽一瓶葡萄酒。"
            },
            {
                "chinese": "森林",
                "pinyin": "sēnlín",
                "usage": "小红帽走在森林小路上。"
            },
            {
                "chinese": "奶奶",
                "pinyin": "nǎinai",
                "usage": "小红帽要去奶奶家。"
            },
            {
                "chinese": "警惕",
                "pinyin": "jǐngtì",
                "usage": "小红帽保持警惕，不告诉狼奶奶的住址。"
            }
        ],
        "grammarPoints": [
            {
                "pattern": "要 + 动词",
                "explanation": "表示打算或计划做某事。",
                "example": "我要去奶奶家。"
            },
            {
                "pattern": "为了 + 动词",
                "explanation": "表示目的。",
                "example": "为了更好地听你说话。"
            }
        ]
    }
}
    """
    
    # Initialize the workflow
    workflow = ScreenplayImageWorkflow(timeout=120, verbose=False)
    
    try:
        print("Initializing workflow with test content")

        # Run the workflow
        print("Running workflow")
        result = await workflow.run(origin_content=test_content)

        # Parse and print the result
        print(f"Workflow completed successfully:{result}")
        
    except Exception as e:
        logger.error("Workflow failed: %s", str(e))
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
