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
    "title": "小红帽的冒险",
    "difficulty": "Intermediate",
    "characters": [
        {
            "name": "小红帽",
            "role": "主角，语言学习者",
            "background": "一个可爱的小姑娘，经常帮助她的奶奶。她喜欢戴着奶奶送的红色丝绒帽子。",
            "personality": "善良、好奇、有时有点天真",
            "languageLevel": "中级",
            "isMainPlayer": true
        },
        {
            "name": "妈妈",
            "role": "支持角色",
            "background": "小红帽的母亲，关心女儿的安全和教育。",
            "personality": "温柔、细心、有责任心",
            "languageLevel": "高级",
            "isMainPlayer": false
        },
        {
            "name": "狼",
            "role": "反派角色",
            "background": "森林中的恶狼，善于欺骗。",
            "personality": "狡猾、贪婪",
            "languageLevel": "中级",
            "isMainPlayer": false
        },
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
            "playerChoiceEvaluate": "如果选择A，小红帽会直接出发；如果选择B，小红帽会再检查一遍东西，但最终还是会出发。",
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
                    "behaviorContent": "蛋糕和葡萄酒。昨天我们家烤了一些蛋糕，可怜的奶奶生了病，要吃一些好东西才能恢复过来。"
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
            "screenContent": "小红帽被周围的美景吸引，开始采花。她越走越深，忘记了时间。与此同时，狼找到了奶奶的家，并吞下了奶奶。",
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
        },
        {
            "playerChoiceEvaluate": "如果选择A，小红帽会立即前往奶奶家；如果选择B，小红帽会继续采花，导致更晚到达。",
            "location": "奶奶家",
            "timeOfDay": "下午",
            "screenContent": "小红帽终于来到了奶奶家。门开着，她感到有些奇怪。她走进屋子，看到奶奶躺在床上，样子非常奇怪。",
            "charactersBehavior": [
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "早上好！"
                },
                {
                    "charactersName": "狼（伪装成奶奶）",
                    "behaviorType": "speaking",
                    "behaviorContent": "哎，乖乖，你的耳朵怎么这样大呀？"
                },
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "为了更好地听你说话呀，乖乖。可是奶奶，你的眼睛怎么这样大呀？"
                },
                {
                    "charactersName": "狼（伪装成奶奶）",
                    "behaviorType": "speaking",
                    "behaviorContent": "为了更清楚地看你呀，乖乖。"
                }
            ],
            "whatNextMainPlayerShouldDo": {
                "question": "你会继续问问题还是逃跑？",
                "answerType": "choose",
                "playerChoice": [
                    {
                        "option": "A",
                        "content": "奶奶，你的手怎么这样大呀？"
                    },
                    {
                        "option": "B",
                        "content": "我觉得不对劲，我应该逃跑。"
                    }
                ]
            }
        },
        {
            "playerChoiceEvaluate": "如果选择A，小红帽会被狼吞掉；如果选择B，小红帽会逃跑并向猎人求助。",
            "location": "奶奶家附近",
            "timeOfDay": "傍晚",
            "screenContent": "小红帽逃出屋子，遇到了一位猎人。猎人决定帮助她。",
            "charactersBehavior": [
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "救命啊！奶奶被狼吞掉了！"
                },
                {
                    "charactersName": "猎人",
                    "behaviorType": "speaking",
                    "behaviorContent": "别怕，小姑娘，我会帮你救出奶奶的。"
                }
            ],
            "whatNextMainPlayerShouldDo": {
                "question": "你会跟猎人一起回去救奶奶吗？",
                "answerType": "choose",
                "playerChoice": [
                    {
                        "option": "A",
                        "content": "是的，我跟你一起去。"
                    },
                    {
                        "option": "B",
                        "content": "太危险了，我还是回家吧。"
                    }
                ]
            }
        },
        {
            "playerChoiceEvaluate": "如果选择A，小红帽会跟猎人一起回去救奶奶；如果选择B，小红帽会回家，但内心不安。",
            "location": "奶奶家",
            "timeOfDay": "晚上",
            "screenContent": "猎人用剪刀剪开了狼的肚子，救出了小红帽和奶奶。狼醒来后试图逃跑，但被石头压死。",
            "charactersBehavior": [
                {
                    "charactersName": "猎人",
                    "behaviorType": "motion",
                    "behaviorContent": "猎人用剪刀剪开狼的肚子，救出了小红帽和奶奶。"
                },
                {
                    "charactersName": "小红帽",
                    "behaviorType": "speaking",
                    "behaviorContent": "真把我吓坏了！狼肚子里黑漆漆的。"
                },
                {
                    "charactersName": "奶奶",
                    "behaviorType": "speaking",
                    "behaviorContent": "谢谢你，猎人。谢谢你救了我们。"
                }
            ],
            "whatNextMainPlayerShouldDo": {
                "question": "你会感谢猎人吗？",
                "answerType": "choose",
                "playerChoice": [
                    {
                        "option": "A",
                        "content": "谢谢你，猎人。你真是太勇敢了！"
                    },
                    {
                        "option": "B",
                        "content": "谢谢你的帮助。"
                    }
                ]
            }
        }
    ],
    "storyProgression": {
        "beginning": "小红帽接受妈妈的嘱托，准备去看望生病的奶奶。",
        "middle": "小红帽在森林中遇到狼，被狼欺骗，差点落入陷阱。后来她意识到危险并寻求猎人的帮助。",
        "end": "猎人救出了小红帽和奶奶，狼被消灭。小红帽学会了警惕和勇敢。"
    },
    "learning": {
        "keyVocabulary": [
            {
                "chinese": "丝绒",
                "pinyin": "sī róng",
                "usage": "奶奶送给小红帽一顶用丝绒做的小红帽。"
            },
            {
                "chinese": "虚弱",
                "pinyin": "xū ruò",
                "usage": "奶奶生病了，身子很虚弱。"
            },
            {
                "chinese": "摔跤",
                "pinyin": "shuāi jiāo",
                "usage": "如果你离开大路，你会摔跤的。"
            },
            {
                "chinese": "盘算",
                "pinyin": "pán suàn",
                "usage": "狼在心中盘算着如何骗过小红帽。"
            },
            {
                "chinese": "警惕",
                "pinyin": "jǐng tì",
                "usage": "小红帽提高了警惕，不再轻易相信陌生人。"
            }
        ],
        "grammarPoints": [
            {
                "pattern": "了",
                "explanation": "表示动作完成或变化发生。",
                "example": "小红帽接受了妈妈的嘱托，出发了。"
            },
            {
                "pattern": "要是...的话",
                "explanation": "表示假设条件。",
                "example": "要是妈妈不允许，我一辈子也不独自离开大路。"
            }
        ]
    }
}
    """