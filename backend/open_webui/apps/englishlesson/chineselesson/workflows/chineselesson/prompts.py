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
     * Relationship to other characters
     * Language proficiency level

3. Scene Design:
   Each scene must include:
   - screenContent: 
     * Detailed environment descriptions, include:Time and location context/Atmosphere and mood setting/Cultural elements naturally woven in
   - playerBehavior: 
     * Natural dialogue progression, the dialogue content need Complete and self-consistent
     * Character interactions that build relationships
     * Non-verbal communication
     * Cultural context and social dynamics
   - playerChoice: 
     * 2-3 meaningful options that:
       > Affect the story direction
       > Impact relationships
       > Vary in language difficulty
       > Lead to different scene outcomes
     * Choices should influence future scenes

4. Learning Integration:
   - Progressive difficulty across scenes
   - Each scene introduces:
     * 3-5 key vocabulary words
     * 1-2 grammar patterns
     * Cultural concepts or customs
   - Natural repetition of previous vocabulary
   - Context-appropriate language use
   - Practical conversation scenarios

5. Cultural Elements:
   - Authentic Chinese customs and traditions
   - Modern Chinese social norms
   - Cultural misunderstanding opportunities
   - Traditional and contemporary elements
   - Regional variations when relevant

Output Format:
{{
    "title": "Story title that reflects the main theme",
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
            "sceneNumber": "Scene number",
            "location": "Where the scene takes place",
            "timeOfDay": "When the scene occurs",
            "screenContent": "Detailed setting and situation description",
            "playerBehavior": {{
                "dialogue": [
                    {{
                        "character": "Speaker name",
                        "content": "the content character say"//the content Complete and self-consistent
                    }}
                ],
                "actions": "Detailed description of actions and body language"
            }},
            "playerChoice": [
                {{
                    "option": "Choice identifier",
                    "content": "Choice content",
                    "consequence": "Immediate and future impact of this choice"
                }}
            ]
        }}
    ],
    "storyProgression": {{
        "beginning": "Setup and initial situation",
        "middle": "Development and complications",
        "end": "Resolution and learning outcomes"
    }},
    "learning":{{
        "keyVocabulary": [
                {{
                    "chinese": "汉字",
                    "pinyin": "Pinyin",
                    "usage": "Example usage in context"
                }}
            ],
            "grammarPoints": [
                {{
                    "pattern": "Grammar pattern",
                    "explanation": "How to use it",
                    "example": "Example in context"
                }}
            ]
    }}
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