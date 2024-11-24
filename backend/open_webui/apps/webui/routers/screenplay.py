from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import dashscope
from dashscope import Generation
import os
import json
import logging

log = logging.getLogger(__name__)
router = APIRouter()

# Make sure your API key is set
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

class ScreenPlay(BaseModel):
    content: str

class GameResponse(BaseModel):
    lesson_id: str
    scene_id: Optional[str] = None
    user_input: Optional[str] = None
    choice_id: Optional[str] = None
    action_type: str
    messages: Optional[list] = None
    course_content: Optional[ScreenPlay] = None
    course_questions: Optional[list] = None

@router.get("/getScreenPlay")
async def getScreenPlay():
    return """
    {
    "title": "小红帽的语言之旅",
    "difficulty": "Beginner",
    "characters": [
        {
            "name": "小红帽",
            "role": "主角，语言学习者",
            "background": "一个可爱的小姑娘，总是戴着一顶红色的丝绒帽子。她善良、好奇，但有时会过于天真。",
            "personality": "天真烂漫、好奇心强、善良",
            "languageLevel": "初学者",
            "isMainPlayer": "true"
        },
        {
            "name": "妈妈",
            "role": "支持角色，指导者",
            "background": "小红帽的母亲，非常关心和保护她的女儿。她经常给小红帽提供生活建议。",
            "personality": "慈爱、谨慎、有责任感",
            "languageLevel": "高级",
            "isMainPlayer": "false"
        },
        {
            "name": "奶奶",
            "role": "支持角色，智慧老人",
            "background": "住在森林里的老奶奶，对小红帽非常疼爱。她经验丰富，喜欢分享智慧。",
            "personality": "慈祥、聪明、有耐心",
            "languageLevel": "中级",
            "isMainPlayer": "false"
        },
        {
            "name": "狼",
            "role": "反派角色，挑战者",
            "background": "一只狡猾的狼，试图欺骗小红帽以达到自己的目的。",
            "personality": "狡猾、贪婪、机智",
            "languageLevel": "中级",
            "isMainPlayer": "false"
        }
    ],
    "scenes": [
        {
            "sceneNumber": 1,
            "location": "小红帽家",
            "timeOfDay": "早晨",
            "screenContent": "清晨的阳光透过窗户照进小红帽的家中。房间里温馨而整洁，桌上放着一块蛋糕和一瓶葡萄酒。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "妈妈",
                        "content": "小红帽，这里有一块蛋糕和一瓶葡萄酒，快给奶奶送去。奶奶生病了，吃了这些就会好一些的。趁着现在天还没有热，赶紧动身吧。在路上要好好走，不要跑，也不要离开大路。"
                    },
                    {
                        "character": "小红帽",
                        "content": "我会小心的，妈妈。"
                    }
                ],
                "actions": "小红帽接过蛋糕和葡萄酒，认真地点点头，与妈妈拉手作保证。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "content": "直接出发去奶奶家",
                    "consequence": "故事继续发展，进入下一个场景。"
                },
                {
                    "option": "B",
                    "content": "先在花园里摘些花再出发",
                    "consequence": "可能会遇到狼，增加故事的复杂性。"
                }
            ]
        },
        {
            "sceneNumber": 2,
            "location": "森林入口",
            "timeOfDay": "上午",
            "screenContent": "小红帽走进了茂密的森林，阳光透过树梢洒下斑驳的光影。四周鸟语花香，景色宜人。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "狼",
                        "content": "你好，小红帽。这么早要去哪里呀？"
                    },
                    {
                        "character": "小红帽",
                        "content": "我要到奶奶家去。"
                    },
                    {
                        "character": "狼",
                        "content": "你那围裙下面有什么呀？"
                    },
                    {
                        "character": "小红帽",
                        "content": "蛋糕和葡萄酒。可怜的奶奶生了病，要吃一些好东西才能恢复过来。"
                    }
                ],
                "actions": "小红帽警惕地看着狼，但并没有表现出恐惧。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "content": "告诉狼奶奶住在哪里",
                    "consequence": "狼会直接去找奶奶，增加故事的紧张感。"
                },
                {
                    "option": "B",
                    "content": "不告诉狼奶奶住在哪里",
                    "consequence": "狼会想办法套出信息，增加对话的复杂性。"
                }
            ]
        },
        {
            "sceneNumber": 3,
            "location": "森林深处",
            "timeOfDay": "中午",
            "screenContent": "小红帽被美丽的花朵吸引，离开了大路，走进了森林深处。四周静悄悄的，只有偶尔传来的鸟鸣声。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "小红帽",
                        "content": "这些花真漂亮，我应该摘一些送给奶奶。"
                    }
                ],
                "actions": "小红帽开始采摘花朵，每采一朵都觉得前面还有更美的。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "content": "继续采摘更多的花",
                    "consequence": "可能错过到达奶奶家的时间，增加故事的紧迫感。"
                },
                {
                    "option": "B",
                    "content": "停止采摘，尽快赶往奶奶家",
                    "consequence": "及时到达奶奶家，避免危险。"
                }
            ]
        },
        {
            "sceneNumber": 4,
            "location": "奶奶家",
            "timeOfDay": "下午",
            "screenContent": "小红帽终于到达了奶奶家，屋门敞开着。屋里显得有些阴暗，给人一种不安的感觉。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "小红帽",
                        "content": "早上好！"
                    },
                    {
                        "character": "狼（伪装成奶奶）",
                        "content": "哎，小红帽，你的耳朵怎么这样大呀？"
                    },
                    {
                        "character": "小红帽",
                        "content": "为了更好地听你说话呀，乖乖。"
                    },
                    {
                        "character": "狼（伪装成奶奶）",
                        "content": "可是奶奶，你的眼睛怎么这样大呀？"
                    },
                    {
                        "character": "小红帽",
                        "content": "为了更清楚地看你呀，乖乖。"
                    },
                    {
                        "character": "狼（伪装成奶奶）",
                        "content": "奶奶，你的嘴巴怎么大得很吓人呀？"
                    },
                    {
                        "character": "小红帽",
                        "content": "可以一口把你吃掉呀！"
                    }
                ],
                "actions": "小红帽感到不对劲，但她还是走向床前，拉开了帘子。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "content": "立刻逃跑",
                    "consequence": "成功逃脱，但可能会惊动狼。"
                },
                {
                    "option": "B",
                    "content": "保持冷静，寻找帮助",
                    "consequence": "有机会等待猎人出现并获得救援。"
                }
            ]
        },
        {
            "sceneNumber": 5,
            "location": "奶奶家",
            "timeOfDay": "傍晚",
            "screenContent": "猎人闯入房间，发现躺在床上的狼。他迅速拿起剪刀，剪开狼的肚子，救出了小红帽和奶奶。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "猎人",
                        "content": "你这老坏蛋，我找了你这么久，真没想到在这里找到你！"
                    },
                    {
                        "character": "小红帽",
                        "content": "真把我吓坏了！狼肚子里黑漆漆的。"
                    },
                    {
                        "character": "奶奶",
                        "content": "谢谢你，猎人。我们真是太幸运了。"
                    }
                ],
                "actions": "小红帽和奶奶感激地看着猎人，三人一起庆祝脱险。"
            },
            "playerChoice": [
                {
                    "option": "A",
                    "content": "感谢猎人并邀请他共进晚餐",
                    "consequence": "增进友谊，结束故事。"
                },
                {
                    "option": "B",
                    "content": "简单道谢后送猎人离开",
                    "consequence": "故事结束，但关系较为平淡。"
                }
            ]
        }
    ],
    "storyProgression": {
        "beginning": "小红帽接到妈妈的任务，准备去看望生病的奶奶。",
        "middle": "小红帽在森林中遇到了狼，被狼骗到了奶奶家。狼吞下了奶奶并伪装成奶奶的样子，企图吞下小红帽。",
        "end": "猎人及时赶到，救出了小红帽和奶奶。小红帽学会了更加谨慎，并感激猎人的帮助。"
    },
    "learning": {
        "keyVocabulary": [
            {
                "chinese": "蛋糕",
                "pinyin": "dàngāo",
                "usage": "妈妈给小红帽准备了一块蛋糕。"
            },
            {
                "chinese": "葡萄酒",
                "pinyin": "pútáojiǔ",
                "usage": "妈妈还给小红帽准备了一瓶葡萄酒。"
            },
            {
                "chinese": "森林",
                "pinyin": "sēnlín",
                "usage": "小红帽走进了茂密的森林。"
            },
            {
                "chinecraft": "鲜花",
                "pinyin": "xiānhuā",
                "usage": "小红帽被美丽的鲜花吸引了。"
            },
            {
                "chinese": "猎人",
                "pinyin": "lièrén",
                "usage": "猎人及时赶到，救出了小红帽和奶奶。"
            }
        ],
        "grammarPoints": [
            {
                "pattern": "要 + 动词",
                "explanation": "表示将要做某事",
                "example": "我要到奶奶家去。"
            },
            {
                "pattern": "为了 + 目的",
                "explanation": "表示做某事的目的",
                "example": "为了更好地听你说话呀，乖乖。"
            }
        ]
    }
}
    """

@router.post("/complateresponse")
async def complateresponse(form_data: GameResponse):
    try:
        log.info(f"Processing game response: {form_data}")
        
        # Default fallback response
        fallback_response = {
            "id": "error",
            "text": "Sorry, there was an error. Please try again.",
            "type": "input"
        }
        
        # Convert messages to conversation format
        conversation_history = ""
        if form_data.messages:
            for msg in form_data.messages:
                role = "Assistant" if msg.get("isBot") else "User"
                conversation_history += f"{role}: {msg.get('content', '')}\n"
        
        # Format course content and questions for the prompt
        course_content = json.dumps(form_data.course_content.dict() if form_data.course_content else {}, indent=2)
        course_questions = json.dumps(form_data.course_questions if form_data.course_questions else [], indent=2)
        
        # Unified prompt combining My Little Pony theme with game mechanics
        prompt = f"""You're a My Little Pony text adventure game made for kids. You're designed to be really fun, so lots of kids like to play.

        Current game state:
        - Action Type: {form_data.action_type}
        - User Input: {form_data.user_input if form_data.user_input else 'None'}
        - Choice Selected: {form_data.choice_id if form_data.choice_id else 'None'}

        Previous conversation:
        {conversation_history}

        The game is around her adventure, where players will make choices based on the course content and questions provided.

        The game content are:
        <CourseContent>
        {course_content}
        </CourseContent>

        The game challenge are:
        <CourseQuestions>
        {course_questions}
        </CourseQuestions>

        The game is suitable for fans of My Little Pony, combining fun, exploration, and decision-making elements that reflect the values of friendship and learning. It includes various paths and endings based on players' choices throughout the adventure.

        Use simple sentences to move the story forward. After 5 game challenges finish, the game will be over with congratulations.

        Generate an appropriate game response in JSON format. The response should:
        1. For new conversations, provide a welcoming message with type "input"
        2. For user inputs, provide feedback and present choices with type "choice"
        3. For user choices, provide feedback and continue the conversation with type "input"

        Response must be in this JSON format:
        {{
            "id": "<scene_id>",
            "text": "<response text>",
            "type": "input" or "choice",
            "choices": [                    // Include only if type is "choice"
                {{"id": "1", "text": "<option 1>"}},
                {{"id": "2", "text": "<option 2>"}}
            ]
        }}

        Make the response fun, engaging, and suitable for kids learning English through My Little Pony adventures."""

        print(f"lesson game Prompt: {prompt}")
        try:
            # Call DashScope API with error handling
            response = Generation.call(
                model='qwen-max',
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )
            
            # Debug logging
            log.info(f"DashScope API Response: {response}")
            
            # Validate response structure
            if not response or not hasattr(response, 'output'):
                log.error("Invalid response structure")
                return fallback_response
            
            # Get the text content from the response
            ai_text = response.output.text
            log.error(f"AI text response: {ai_text}")
            
            try:
                # Parse the JSON from the text content
                parsed_response = json.loads(ai_text)
                
                # Validate required fields
                if not all(key in parsed_response for key in ['id', 'text', 'type']):
                    log.error(f"Missing required fields in parsed response: {parsed_response}")
                    return fallback_response
                
                log.info(f"Successfully parsed response: {parsed_response}")
                return parsed_response
                
            except json.JSONDecodeError as je:
                log.error(f"JSON parsing error: {str(je)}")
                return fallback_response
                
        except Exception as api_error:
            log.error(f"DashScope API error: {str(api_error)}")
            return fallback_response
            
    except Exception as e:
        log.error(f"Error processing game response: {str(e)}")
        return fallback_response
