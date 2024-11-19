from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
from dashscope import Generation
import json
from prompts import *
import logging
from typing import Union
import os
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessons
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
            screenplay = response.output.text
            print(f"Generated screenplay:{screenplay}")
            
            return ReviewScreenplayEvent(screenplay=screenplay, original_content=ev.content)
        except Exception as e:
            logger.error("Failed to generate screenplay: %s", str(e))
            raise

    @step
    async def step_review_screenplay(self, ev: ReviewScreenplayEvent) -> Union[GenerateScreenplayEvent | StopEvent]:
        print("Reviewing generated screenplay")
        prompt = prompt_review_screenplay.format(
            screenplay=ev.screenplay, 
            original_content=ev.original_content
        )
        try:
            response = Generation.call(
                model='qwen-max',
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )
            review_result = response.output.text
            print(f"Review result: {review_result}")
            
            if "approved" in review_result.lower():
                print("Screenplay approved, proceeding to scene generation")
                return StopEvent(result=review_result)
            print("Screenplay needs revision, generating new version")
            return GenerateScreenplayEvent(content=ev.original_content)
        except Exception as e:
            logger.error("Failed to review screenplay: %s", str(e))
            raise

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
        await save_chinese_lesson(result)
        
    except Exception as e:
        logger.error("Workflow failed: %s", str(e))
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
