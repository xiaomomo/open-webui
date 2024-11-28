prompt_generate_screenplay = """
Generate a comprehensive and engaging Chinese language learning screenplay that tells a complete story arc:

Input Content:
<content>
{content}
</content>

Requirements:
1. Story Structure:
   - Complete story arc with beginning, middle, and end
   - 3-10 interconnected scenes that build upon each other
   - Clear progression of language difficulty
   - Coherent narrative thread linking all scenes
   - Meaningful character development throughout

2. Characters:
   - One main player (the language learner)
   - 1-5 recurring supporting characters who:
     * Have distinct personalities and backgrounds
     * Develop relationships with the player
     * Use consistent speech patterns
     * Appear across multiple scenes
   - Each character profile includes:
     * Name
     * Personality traits and quirks
     * Background story

3. Scene Design:
   Each scene must include:
   - screenContent:
     * Detailed environment descriptions, include:Time and location context/Atmosphere and mood setting/Cultural elements naturally woven in
   - playerBehavior:
     * Natural dialogue progression, the dialogue content need Complete and self-consistent
     * Character interactions that build relationships
     * Non-verbal communication
   - playerChoice:
     * 2-3 meaningful options that:
       > Affect the story direction
       > Impact relationships
       > Vary in language difficulty
       > Lead to different scene outcomes
     * Choices should influence future scenes

Output Format:
{{
    "title": "Story title that reflects the main theme",
    "opening_remarks":"",//opening_remarks
    "difficulty": "Beginner/Intermediate/Advanced",
    "characters": [
        {{
            "name": "Character name",
            "role": "Role in story",
            "background": "Character background",
            "personality": "Key traits",
            "languageLevel": "Proficiency level",
            "isMainPlayer":"true or false"// does this character is main role of the screenPlay
        }}
    ],
    "scenes": [
        {{
            "playerChoiceEvaluate":"give evaluate of playerChoice", //exist if has user choice
        "location": "Where the scene takes place",
            "timeOfDay": "When the scene occurs",
            "screenContent": "Detailed setting and situation description",

            "charactersBehavior":[
                {{
                "charactersName":"",
                "behaviorType":"thinking/speaking/motion",
                "behaviorContent":""
                }}
            ]
            "whatNextMainPlayerShouldDo": {{
                "question":"",
                "answerType":"choose/input"
                "playerChoice": [
                {{
                    "option": "",
                    "content": "Choice content"
                }}
            ]
            }}

        }}
    ]
}}

Remember to:
1. Maintain narrative consistency across all scenes
2. Ensure each choice has meaningful consequences that affect later scenes
3. Balance language learning with storytelling
4. Create memorable character interactions
5. Include cultural elements naturally within the story
6. Make sure the story reaches a satisfying conclusion
7. all Characters come from the content
"""

prompt_review_screenplay = """
Review the following Chinese language learning screenplay and evaluate its effectiveness:

Screenplay: {screenplay}
Original Content Requirements: {original_content}

Please analyze the following aspects and provide specific feedback:

1. Educational Value:
   - Are the language learning objectives clear and appropriate?
   - Is the difficulty level consistent?
   - Are vocabulary and grammar points properly introduced and practiced?

2. Engagement and Interactivity:
   - Are the player choices meaningful and educational?
   - Is the story engaging and culturally relevant?
   - Do the scenes flow logically?

3. Technical Structure:
   - Is the JSON format correct and complete?
   - Are all required elements present (screenContent, playerBehavior, playerChoice)?

4. Cultural Accuracy:
   - Is the cultural content authentic and nuanced?
   - Are social interactions portrayed with appropriate subtlety?
   - Are cultural references naturally integrated into the story?

5. Emotional Impact:
   - Does the screenplay create memorable moments?
   - Are character relationships believable and developing?
   - Is there appropriate humor or drama?

Please respond in the following format:
{{
    "approved": true/false,
    "score": (1-10),
    "issues": [
        {{
            "category": "category_name",
            "description": "issue_description",
            "suggestion": "improvement_suggestion"
        }}
    ],
    "overall_feedback": "summary_text"
}}
"""
prompt_generate_core_info = """
You’re an information extractor skilled in analyzing and summarizing narrative text. Your expertise lies in identifying key elements such as Subject, Environment, Activity, Emotion, Color Palette, and Lighting from various scenarios. 

Your task is to extract information from the provided text snippet. Here’s the input you need to analyze: 
Here is one example:

< input>
{{  
            "sceneNumber": 3,            "location": "马棚",  
            "timeOfDay": "中午",  
            "screenContent": "小马回到了马棚，老马正坐在那里休息。马棚里依旧温暖而宁静。",  
            "playerBehavior": {{                "dialogue": [                    {{                        "character": "老马",  
                        "chinese": "怎么回来啦？"  
                    }},                    {{                        "character": "小马",  
                        "chinese": "一条河挡住了去路，我过不去。"  
                    }},                    {{                        "character": "老马",  
                        "chinese": "那条河不是很浅吗？"  
                    }},                    {{                        "character": "小马",  
                        "chinese": "是呀！牛伯伯也这么说。可是松鼠说河水很深，还淹死过他的伙伴呢！"  
                    }},                    {{                        "character": "老马",  
                        "chinese": "那么河水到底是深还是浅呢？你仔细想过他们的话吗？"  
                    }},                    {{                        "character": "小马",  
                        "chinese": "没...没想过。"  
                    }},                    {{                        "character": "老马",  
                        "chinese": "孩子，光听别人说，自己不动脑筋，不去试试，是不行的。河水是深是浅，你去试一试，就知道了。"  
                    }}                ],                "actions": "小马低下了头，显得有些羞愧。老马则用温柔的眼神看着他。"  
            }}
</input>

<output>
- Subject: _老马和小马_
- Environment: _马棚里_
- Action/Activity: _聊天_
- Mood/Emotion: _宁静，温柔_
- Color Palette: _温暖_
- Lighting: _温暖_
- Style/Aesthetic: _卡通_
</output>

Now It's your time to extract information
< input>
{scene}
</input>
"""

prompt_generate_overview_core_info = """
You’re an information extractor skilled in analyzing and summarizing narrative text. Your expertise lies in identifying key elements such as Subject, Environment, Activity, Emotion, Color Palette, and Lighting from various scenarios. 

Your task is to extract information from the provided text snippet. Here’s the input you need to analyze: 
Here is one example:

< input>
从前有个可爱的小姑娘，谁见了都喜欢，但最喜欢她的是她的奶奶，简直是她要什么就给她什么。 一次，奶奶送给小姑娘一顶用丝绒做的小红帽，戴在她的头上正好合适。 从此，姑娘再也不愿意戴任何别的帽子，于是大家便叫她"小红帽"。
一天，妈妈对小红帽说："来，小红帽，这里有一块蛋糕和一瓶葡萄酒，快给奶奶送去，奶奶生病了，身子很虚弱，吃了这些就会好一些的。趁着现在天还没有热，赶紧动身吧。在路上要好好走，不要跑，也不要离开大路，否则你会摔跤的，那样奶奶就什么也吃不上了。到奶奶家的时候，别忘了说'早上好'，也不要一进屋就东瞧西瞅。"
"我会小心的。"小红帽对妈妈说，并且还和妈妈拉手作保证。
奶奶住在村子外面的森林里，离小红帽家有很长一段路。 小红帽刚走进森林就碰到了一条狼。 小红帽不知道狼是坏家伙，所以一点也不怕它。
"你好，小红帽，"狼说。
"谢谢你，狼先生。"
"小红帽，这么早要到哪里去呀？"
"我要到奶奶家去。"
"你那围裙下面有什么呀？"
"蛋糕和葡萄酒。昨天我们家烤了一些蛋糕，可怜的奶奶生了病，要吃一些好东西才能恢复过来。"
"你奶奶住在哪里呀，小红帽？"
"进了林子还有一段路呢。她的房子就在三棵大橡树下，低处围着核桃树篱笆。你一定知道的。"小红帽说。
狼在心中盘算着："这小东西细皮嫩肉的，味道肯定比那老太婆要好。我要讲究一下策略，让她俩都逃不出我的手心。"于是它陪着小红帽走了一会儿，然后说："小红帽，你看周围这些花多么美丽啊！干吗不回头看一看呢？还有这些小鸟，它们唱得多么动听啊！你大概根本没有听到吧？林子里的一切多么美好啊，而你却只管往前走，就像是去上学一样。"
小红帽抬起头来，看到阳光在树木间来回跳荡，美丽的鲜花在四周开放，便想："也许我该摘一把鲜花给奶奶，让她高兴高兴。现在天色还早，我不会去迟的。"她于是离开大路，走进林子去采花。 她每采下一朵花，总觉得前面还有更美丽的花朵，便又向前走去，结果一直走到了林子深处。
就在此时，狼却直接跑到奶奶家，敲了敲门。
"是谁呀？"
"是小红帽。"狼回答，"我给你送蛋糕和葡萄酒来了。快开门哪。"
"你拉一下门栓就行了，"奶奶大声说，"我身上没有力气，起不来。"
狼刚拉起门栓，那门就开了。 狼二话没说就冲到奶奶的床前，把奶奶吞进了肚子。 然后她穿上奶奶的衣服，戴上她的帽子，躺在床上，还拉上了帘子。
可这时小红帽还在跑来跑去地采花。 直到采了许多许多，她都拿不了啦，她才想起奶奶，重新上路去奶奶家。
看到奶奶家的屋门敞开着，她感到很奇怪。 她一走进屋子就有一种异样的感觉，心中便想："天哪！平常我那么喜欢来奶奶家，今天怎么这样害怕？"她大声叫道："早上好！"，可是没有听到回答。 她走到床前拉开帘子，只见奶奶躺在床上，帽子拉得低低的，把脸都遮住了，样子非常奇怪。
"哎，奶奶，"她说，"你的耳朵怎么这样大呀？"
"为了更好地听你说话呀，乖乖。"
"可是奶奶，你的眼睛怎么这样大呀？"小红帽又问。
"为了更清楚地看你呀，乖乖。"
"奶奶，你的手怎么这样大呀？"
"可以更好地抱着你呀。"
"奶奶，你的嘴巴怎么大得很吓人呀？"
"可以一口把你吃掉呀！"
狼刚把话说完，就从床上跳起来，把小红帽吞进了肚子，狼满足了食欲之后便重新躺到床上睡觉，而且鼾声震天。 一位猎人碰巧从屋前走过，心想："这老太太鼾打得好响啊！我要进去看看她是不是出什么事了。"猎人进了屋，来到床前时却发现躺在那里的竟是狼。 "你这老坏蛋，我找了你这么久，真没想到在这里找到你！"他说。 他正准备向狼开枪，突然又想到，这狼很可能把奶奶吞进了肚子，奶奶也许还活着。 猎人就没有开枪，而是操起一把剪刀，动手把呼呼大睡的狼的肚子剪了开来。 他刚剪了两下，就看到了红色的小帽子。 他又剪了两下，小姑娘便跳了出来，叫道："真把我吓坏了！狼肚子里黑漆漆的。"接着，奶奶也活着出来了，只是有点喘不过气来。 小红帽赶紧跑去搬来几块大石头，塞进狼的肚子。 狼醒来之后想逃走，可是那些石头太重了，它刚站起来就跌到在地，摔死了。
三个人高兴极了。 猎人剥下狼皮，回家去了；奶奶吃了小红帽带来的蛋糕和葡萄酒，精神好多了；而小红帽却在想："要是妈妈不允许，我一辈子也不独自离开大路，跑进森林了。"
人们还说，小红帽后来又有一次把蛋糕送给奶奶，而且在路上又有一只狼跟她搭话，想骗她离开大路。 可小红帽这次提高了警惕，头也不回地向前走。 她告诉奶奶她碰到了狼，那家伙嘴上虽然对她说"你好"，眼睛里却露着凶光，要不是在大路上，它准把她给吃了。 "那么，"奶奶说，"我们把门关紧，不让它进来。"不一会儿，狼真的一面敲着门一面叫道："奶奶，快开门呀。我是小红帽，给你送蛋糕来了。"但是她们既不说话，也不开门。 这长着灰毛的家伙围着房子转了两三圈，最后跳上屋顶，打算等小红帽在傍晚回家时偷偷跟在她的后面，趁天黑把她吃掉。 可奶奶看穿了这家伙的坏心思。 她想起屋子前有一个大石头槽子，便对小姑娘说："小红帽，把桶拿来。我昨天做了一些香肠，提些煮香肠的水去倒进石头槽里。"小红帽提了很多很多水，把那个大石头槽子装得满满的。 香肠的气味飘进了狼的鼻孔，它使劲地用鼻子闻呀闻，并且朝下张望着，到最后把脖子伸得太长了，身子开始往下滑。 它从屋顶上滑了下来，正好落在大石槽中，淹死了。 小红帽高高兴兴地回了家，从此再也没有谁伤害过她。
</input>

<output>
- Subject: _小姑娘、狼_
- Environment: _森林里_
- Action/Activity: _送蛋糕给奶奶_
- Mood/Emotion: _宁静_
- Color Palette: _温暖_
- Lighting: _温暖_
- Style/Aesthetic: _卡通_
</output>

Now It's your time to extract information
< input>
{scene}
</input>
"""

reduce_prompt = """
help me reduce the article to 1000 words. keep the story arc and the main character.
<input>
{content}
</input>
"""