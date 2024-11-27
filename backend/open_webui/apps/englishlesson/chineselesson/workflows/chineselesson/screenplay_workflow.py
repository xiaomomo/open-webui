from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
from dashscope import Generation
import json
# from .prompts import *
from prompts import *
import logging
from typing import Union
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../')))
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessonModel, FredisaLessons

from open_webui.apps.englishlesson.workflows.lesson_question.lesson_question import LessonQuestionWorkflow

# Create logger instance
logger = logging.getLogger(__name__)


class GenerateScreenplayEvent(Event):
    content: str

class ReviewScreenplayEvent(Event):
    screenplay: str
    original_content: str

class ScreenplayWorkflow(Workflow):
    @step
    async def step_start(self, ev: StartEvent) -> GenerateScreenplayEvent:
        print(f"Starting workflow with content:{ev.origin_content}")
        return GenerateScreenplayEvent(content=ev.origin_content)

    @step
    async def step_generate_screenplay(self, ev: GenerateScreenplayEvent) -> ReviewScreenplayEvent:
        print("Generating screenplay from content")
        prompt = prompt_generate_screenplay.format(content=ev.content)
        try:
            print(f"llm start:{prompt}")
            response = Generation.call(
                model='qwen-max',
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )
            # Check if response is valid and has the expected structure
            if not response or not hasattr(response, 'output'):
                raise ValueError("Invalid response from Generation.call")
                
            # Access the response text - adjust this based on the actual response structure
            screenplay = response.output.get('text', '')
            if not screenplay:
                raise ValueError("No screenplay text generated")
                
            print(f"Generated screenplay:{screenplay}")
            return ReviewScreenplayEvent(screenplay=screenplay, original_content=ev.content)
        except Exception as e:
            logger.error("Failed to generate screenplay: %s", str(e))
            raise

    @step
    async def step_review_screenplay(self, ev: ReviewScreenplayEvent) -> Union[GenerateScreenplayEvent | StopEvent]:
        print("Reviewing generated screenplay")
        # prompt = prompt_review_screenplay.format(
        #     screenplay=ev.screenplay,
        #     original_content=ev.original_content
        # )
        # try:
        #     response = Generation.call(
        #         model='qwen-max',
        #         messages=[
        #             {'role': 'user', 'content': prompt}
        #         ]
        #     )
        #     review_result = response.output.text
        #     print(f"Review result: {review_result}")
        #
        #     if "approved" in review_result.lower():
        #         print("Screenplay approved, proceeding to scene generation")
        #         return StopEvent(result=review_result)
        #     print("Screenplay needs revision, generating new version")
        #     return GenerateScreenplayEvent(content=ev.original_content)
        # except Exception as e:
        #     logger.error("Failed to review screenplay: %s", str(e))
        #     raise
        print("Screenplay approved, proceeding to scene generation")
        return StopEvent(result=ev.screenplay)

# maybe can you new table, for new form
async def save_chinese_lesson(content):
    fredisaLesson = FredisaLessonForm(
        unit=content.get('title', ''),  # Assuming the result has a 'title' field
        subject="Chinese",
        content=content.get('raw_content', ''),
        lesson_json=content,
        question_json="",
        lesson_img=""
    )

    # Generate questions using the LessonQuestionWorkflow
    w = LessonQuestionWorkflow(timeout=120, verbose=False)
    question_json = await w.run(origin_content=fredisaLesson.lesson_json)
    print(f"workflow generate question_json:{question_json}")
    fredisaLesson.question_json = question_json

    # Save to database
    lesson = FredisaLessons.insert_new_lesson(fredisaLesson)
    return lesson

async def main():
    print("Starting main workflow execution")
    # Test content
    test_content = """
从前有个女孩，非常懒惰，怎么着都不愿意纺纱。终于有一天，母亲感到忍无可忍，就打了她一顿，她于是嚎啕大哭起来。 正巧这时王后乘车从门前经过，听见了哭声，吩咐把车停下来，进屋问那位母亲为什么打女儿。 做母亲的怎亚麻，她愿意纺多少就纺多少。"母亲听了这话，打心眼儿里高兴，满口答应下来，王后便带着女孩走了。她们到了王宫之后，王后领着女孩上了楼，把三间库房指给她看，只见库房里装满了最好的亚麻。 "喏，你就为我纺这些亚麻你什么时候纺完了，就嫁给我的长子。"女孩听了心里一阵惊恐--即使她每天从早纺到晚，纺到她三百岁的时候，也休想把那么多的亚麻纺完。 剩下女孩独自一人时，她就哭了起来。 她就这样哭哭啼啼地坐着，一晃儿三天过去了，三个女人走到窗下停住了脚，问女孩为什么忧心忡忡，她就向她们诉说了自己的苦恼。 "只要你不嫌我们丢人，"他们对女孩说道，"请我们参加你的婚礼，说我们是你的表姐，并且让我们与你同桌喝喜酒，我们就帮你把这些亚麻纺完相奇特的女人进屋来。 她们进来后刚一坐下就开始纺纱。 每次王后来，女孩生怕王后发现，便把那三个纺纱女藏起来，而让王后看已经纺好的纱。 王后看了之后，对她赞不绝口。库房里所有的亚麻都纺完了，这三个纺织女便跟女非常好。在我自己幸福如意的时候，怎么也不愿意冷漠了她们。请允许我邀请她们来参加婚礼，并且让她们在婚宴上和我们坐在一起。"王后和王子欣然同意。 婚礼那天，三个纺纱女果然来了。 她们打扮得怪模怪样的，很令人发笑随后，他转身走到那个大脚板女人身边，问道："您的一只脚怎么会这样大呢？""踏纺车踏的呗。"她回答道。新郎又走到第二个女人身旁，问道："您的嘴唇怎么会耷拉着呢？""舔麻线舔的呗。"她回答说。然后他问第三个女人："您
    """
    
    # Initialize the workflow
    workflow = ScreenplayWorkflow(timeout=120, verbose=False)
    
    try:
        print("Initializing workflow with test content")

        # Run the workflow
        print("Running workflow")
        result = await workflow.run(origin_content=test_content)

        # Parse and print the result
        print(f"Workflow completed successfully:{result}")
        # await save_chinese_lesson(result)
        
    except Exception as e:
        logger.error("Workflow failed: %s", str(e))
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# if __name__ == '__main__':
#     prompt = """
#
# Generate a comprehensive and engaging Chinese language learning screenplay that tells a complete story arc:
#
# Input Content:
# <content>
# 从前，有个男人死了妻子，有个女人死了丈夫。 这个男人有个女儿，这个女人也有个女儿。 两个小姑娘互相认识，经常一起出去散步。 有一天，她们散完步后一起来到女人的家里，女人对男人的女儿说："听着，告诉你爸爸，说我愿意嫁给他，从此你天天早晨都能用牛奶洗脸，还能喝上葡萄酒，而我自己的女儿只能用水洗脸，也只能喝清水。"小姑娘回到家中，把女人的话告诉了她爸爸。 男人说："我该怎么办呢？结婚是喜事，可也会带来痛苦。"他迟迟拿不定主意，最后脱下一只靴子，说："这只靴子的底上有个洞。你把它拎到阁楼上去，把它挂在一根大钉子上，然后往里面灌些水。要是水没有漏出来，我就再娶个妻子；可要是水漏了出来，我就不娶。"姑娘按她父亲所说的办了。 可是水使得洞胀拢了，靴子里灌满了水也没有漏出来。 她把结果告诉了她父亲，父亲又亲自上来察看，看到情况果然如此，便去向那寡妇求婚，然后举行了婚礼。第一天早晨，两个姑娘起来后，在男人的女儿的面前果然放着洗脸的牛奶和喝的葡萄酒，而在女人的女儿的面前放着的只有洗脸的清水和喝的清水。 第二天早晨，男人的女儿和女人的女儿的面前都放着洗脸的清水和喝的清水。 到了第三天早晨，男人的女儿的面前放着洗脸用的清水和喝的清水，而女人的女儿的面前却放着洗脸用的牛奶和喝的葡萄酒。 以后天天都是这样。 那女人成了她继女的死敌，对她一天坏似一天，她还万分嫉妒她的继女，因为她的继女美丽可爱，而她自己的女儿又丑又令人讨厌。冬天到了，一切都冻得像石头一样硬，山顶和山谷都被大雪覆盖着。 一天，女人用纸做了件衣服，把她的继女叫过来，说："听着，你穿上这件衣服，到森林里去给我采一篮草莓，我很想吃。""天哪！"姑娘说，"冬天怎么会有草莓呢？地上都结了冰，大雪把一切都盖住了，再说，我怎么能穿着这身纸衣服出去呢？外面冷得连呼出的气都能冻起来。风会往这衣服里面吹，荆棘也会把它挂破的。""你敢跟我顶嘴？"继母说，"你快给我去！要是没有采到一篮草莓，你就别想回来！"然后她又给姑娘一小块硬梆梆的面包，说："这是你一天的口粮，"心里却在想："你在外面不会冻死也会饿死的，别想再回来烦我。"姑娘只好顺从地穿上纸衣服，提着篮子走了出去。 外面一片冰天雪地，连一棵绿草都找不到。 她来到森林里后，看到一座小房子，里面有三个小矮人在向外张望。 她向他们问好 ，然后轻轻地敲了敲门。 他们叫"进来"，她便走进屋，坐在炉子旁的长凳上烤火，吃她的早饭。 小矮人们说："也分一点给我们吧。""好的，"她说着便把面包掰成两半，给了他们一半。 他们问："你大冬天穿着这身薄薄的衣服到森林里来干吗？""唉，"她回答，"我得采一篮草莓，否则我就回不了家了。"等她吃完面包后，他们递给她一把扫帚，说："去帮我们把后门的雪扫掉吧。"可等她出去后，三个小矮人却商量了起来："她这么可爱，又把面包分给了我们，我们送她什么好呢？"第一个矮人说："我送给她的礼物是：她一天比一天更美丽。"第二个矮人说："我送给她的礼物是：她一开口说话就吐出金子来。"第三个矮人说："我送给她的礼物是：一个国王娶她当王后。"姑娘这时正按照他们的吩咐，用扫帚把小屋后面的雪扫掉。 她看到了什么？ 雪下面露出了红彤彤的草莓！ 她高兴极了，赶紧装了满满一篮子，谢了小矮人，还和他们一一握手道别，然后带着她继母垂涎的东西跑回家去了。 谁知，她进门刚说了声"晚上好"，嘴里就掉出来一块金子！ 于是，她把自己在森林里遇到的事情讲了出来，而且每讲一句，嘴里就掉出来一块金子，弄得家里很快就堆满了金子。 "瞧她那副德行！"继母的女儿嚷道，"就这样乱扔金子！"她心里嫉妒得要命，也渴望着到森林里去采草莓。 她母亲却说："不行，我的好女儿，外面太冷了，你会冻死的。"可是她女儿缠着不放，她最后只好让步。 她给女儿缝了件皮袄，硬要她穿上；然后又给她抹了黄油的面包和蛋糕，让她带着路上吃。这个姑娘进了森林之后，径直向小屋走去。 三个小矮人又在屋里向外张望，可是她根本不和他们打招呼，既不看他们，也不和他们说话，大摇大摆地走进屋，一屁股坐到炉子旁，吃起自己的面包和蛋糕来。 "分一点给我们吧，"小矮人们说；可是她却回答："这都不够我自己吃的，怎么能分给别人呢？"等她吃完，他们又说："这里有把扫帚，把后门的雪扫干净。"她回答："我又不是你们的佣人。"看到他们不会给她任何礼物了，她便自己冲出了屋子。 三个小矮人商量道："像她这种坏心肠的小懒鬼，又不肯施舍给别人东西，我们该送她什么呢？"第一个矮人说："我让她长得一天比一天丑！"第二个矮人说："我让她一开口说话就从嘴里跳出一只癞蛤蟆！"第三个矮人说："我让她不得好死！"姑娘在屋外找草莓，可一个也找不到，只好气鼓鼓地回家去了。 她开口给母亲讲自己在森林里的遭遇，可是，她每讲一句话，嘴里就跳出来一只癞蛤蟆，把大家都吓坏了。这一来继母更是气坏了，千方百计地盘算着怎么折磨丈夫的女儿，可是这姑娘却长得一天比一天更美。 终于，继母取出一只锅子，架在火堆上 ，在里面煮线团。 线团煮过之后，她把它捞出来，搭在姑娘的肩膀上，然后又给姑娘一把斧头，让她去结冰的小河，在冰面上凿一个洞，在洞里漂洗线团。 姑娘顺从地来到河边，走到河中央凿冰。 她正凿着，岸上驶来了一辆华丽的马车，里面坐着国王。 马车停了下来，国王问："姑娘，你是谁？在这里干什么？""我是个可怜的女孩，在这里漂洗线团。"国王很同情她，而且又看到她长得这么美丽，便对她说："你愿意和我一起走吗？""当然愿意啦。"她回答，因为她非常高兴能离开继母和继母的女儿。 姑娘坐到国王的马车上，和国王一起回到宫中。 他俩立刻就举行了婚礼，正像三个小矮人许诺过的一样。 一年后，年轻的王后生下了一个儿子。 她的继母早已听说她交上了好运，这时也带着亲生女儿来到王宫，假装是来看王后的。 可是看到国王刚出去，而且旁边又没有别人，这坏心肠的女人就抓住王后的头，她的女儿抓住王后的脚，把她从床上抬下来，从窗口把她扔进了外面的大河里。 然后，继母的丑女儿躺在床上，老婆子从头到脚把她盖了起来。 当国王回到房间，想和他的妻子说话的时候，老婆子叫了起来："嘘，唬，不要打搅她，她现在正在发汗。今天不要打搅她。"国王丝毫没有怀疑，一直等到第二天早晨才过来。 他和妻子说话，谁知她刚开口，嘴里就跳出来一只癞蛤蟆，而不像从前那样掉出金子来。 国王问这是怎么回事，老婆子便说这是发汗发出来的，很快就会好的。 但是当天夜里，王宫里的小帮工看见一只鸭子从下水道里游了出来，而且听见它说："国王，你在做什么？你是睡着了还是醒着？ "看到小帮工没有回答，它又说："我的两位客人在做什么？"小帮工说："她们睡熟了。"鸭子又问："我的小宝宝在做什么？"小帮工回答："他在摇篮里睡得好好的。"鸭子变成了王后的模样，上去给孩子喂奶，摇着他的小床，给他盖好被子，然后又变成鸭子，从下水道游走了。 她这样一连来了两个晚上，第三天晚上，她对小帮工说："你去告诉国王，让他带上他的宝剑，站在门槛上，在我的头上挥舞三下。"小帮工赶紧跑去告诉国王，国王提着宝剑来了，在那幽灵的头顶上挥舞了三下。 他刚舞到第三下，她的妻子就站在了他的面前，像以前一样健康强壮。 国王高兴极了，可他仍然把王后藏进密室，等着礼拜天婴儿受洗的日子到来。 洗礼结束之后，他说："要是有人把别人从床上拖下来，并且扔进河里，这个人该受到什么样的惩罚？"老婆子说："对这样坏心肠的人，最好的惩罚是把他装进里面插满了钉子的木桶，从山坡上滚到河里去。""那么，"国王说，"你已经为自己做出了判决。"国王命令搬来一只这样的木桶，把老婆子和她的女儿装进去，并且把桶盖钉死，把桶从山坡上滚了下去，一直滚到河心。
# </content>
#
# Requirements:
# 1. Story Structure:
#    - Complete story arc with beginning, middle, and end
#    - 3-10 interconnected scenes that build upon each other
#    - Clear progression of language difficulty
#    - Coherent narrative thread linking all scenes
#    - Meaningful character development throughout
#
# 2. Characters:
#    - One main player (the language learner)
#    - 1-5 recurring supporting characters who:
#      * Have distinct personalities and backgrounds
#      * Develop relationships with the player
#      * Use consistent speech patterns
#      * Appear across multiple scenes
#    - Each character profile includes:
#      * Name
#      * Personality traits and quirks
#      * Background story
#      * Relationship to other characters
#      * Language proficiency level
#
# 3. Scene Design:
#    Each scene must include:
#    - screenContent:
#      * Detailed environment descriptions, include:Time and location context/Atmosphere and mood setting/Cultural elements naturally woven in
#    - playerBehavior:
#      * Natural dialogue progression, the dialogue content need Complete and self-consistent
#      * Character interactions that build relationships
#      * Non-verbal communication
#      * Cultural context and social dynamics
#    - playerChoice:
#      * 2-3 meaningful options that:
#        > Affect the story direction
#        > Impact relationships
#        > Vary in language difficulty
#        > Lead to different scene outcomes
#      * Choices should influence future scenes
#
# 4. Learning Integration:
#    - Progressive difficulty across scenes
#    - Each scene introduces:
#      * 3-5 key vocabulary words
#      * 1-2 grammar patterns
#      * Cultural concepts or customs
#    - Natural repetition of previous vocabulary
#    - Context-appropriate language use
#    - Practical conversation scenarios
#
# 5. Cultural Elements:
#    - Authentic Chinese customs and traditions
#    - Modern Chinese social norms
#    - Cultural misunderstanding opportunities
#    - Traditional and contemporary elements
#    - Regional variations when relevant
#
# Output Format:
# {
#     "title": "Story title that reflects the main theme",
#     "opening_remarks":"",//opening_remarks
#     "difficulty": "Beginner/Intermediate/Advanced",
#     "characters": [
#         {
#             "name": "Character name",
#             "role": "Role in story",
#             "background": "Character background",
#             "personality": "Key traits",
#             "languageLevel": "Proficiency level",
#             "isMainPlayer":"true or false"// does this character is main role of the screenPlay
#         }
#     ],
#     "scenes": [
#         {
#             "playerChoiceEvaluate":"give evaluate of playerChoice", //exist if has user choice
#         "location": "Where the scene takes place",
#             "timeOfDay": "When the scene occurs",
#             "screenContent": "Detailed setting and situation description",
#
#             "charactersBehavior":[
#                 {
#                 "charactersName":"",
#                 "behaviorType":"thinking/speaking/motion",
#                 "behaviorContent":""
#                 }
#             ]
#             "whatNextMainPlayerShouldDo": {
#                 "question":"",
#                 "answerType":"choose/input"
#                 "playerChoice": [
#                 {
#                     "option": "",
#                     "content": "Choice content"
#                 }
#             ]
#             }
#
#         }
#     ],
#     "storyProgression": {
#         "beginning": "Setup and initial situation",
#         "middle": "Development and complications",
#         "end": "Resolution and learning outcomes"
#     },
#     "learning":{
#         "keyVocabulary": [
#                 {
#                     "chinese": "汉字",
#                     "pinyin": "Pinyin",
#                     "usage": "Example usage in context"
#                 }
#             ],
#             "grammarPoints": [
#                 {
#                     "pattern": "Grammar pattern",
#                     "explanation": "How to use it",
#                     "example": "Example in context"
#                 }
#             ]
#     }
# }
#
# Remember to:
# 1. Maintain narrative consistency across all scenes
# 2. Ensure each choice has meaningful consequences that affect later scenes
# 3. Balance language learning with storytelling
# 4. Create memorable character interactions
# 5. Include cultural elements naturally within the story
# 6. Make sure the story reaches a satisfying conclusion
# 7. all Characters come from the content
#         """
#     response = Generation.call(
#         model='qwen-max',
#         messages=[
#             {'role': 'user', 'content': prompt}
#         ]
#     )
#     print(response.output.text)