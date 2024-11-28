from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)
from dashscope import Generation
import json
from .prompts import *
# from prompts import *
import logging
from typing import Union
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../../')))
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessonModel, FredisaLessons

from open_webui.apps.englishlesson.workflows.lesson_question.lesson_question import LessonQuestionWorkflow

# Create logger instance
logger = logging.getLogger(__name__)

class ReduceContentEvent(Event):
    content: str

class GenerateScreenplayEvent(Event):
    content: str

class ReviewScreenplayEvent(Event):
    screenplay: str
    original_content: str

class ScreenplayWorkflow(Workflow):
    @step
    async def step_start(self, ev: StartEvent) -> ReduceContentEvent:
        print(f"Starting workflow with content:{ev.origin_content}")
        return ReduceContentEvent(content=ev.origin_content)

    @step
    async def reduce_content_screenplay(self, ev: ReduceContentEvent) -> GenerateScreenplayEvent:
        print("reduce_content_screenplay")
        prompt = reduce_prompt.format(content=ev.content)
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
            reduce_content = response.output.get('text', '')
            if not reduce_content:
                raise ValueError("No screenplay text generated")

            print(f"reduce_content content:{reduce_content}")
            return GenerateScreenplayEvent(content=reduce_content)
        except Exception as e:
            logger.error("Failed to generate screenplay: %s", str(e))
            raise

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
很久以前，有一位老国王病重。他意识到自己时日无多，便召见了忠诚的仆间挂着金屋公主画像的房间。因为那幅画中的女子美丽无比，会让看到的人陷入无法自拔的爱恋中。约翰承诺会尽忠职守，即便牺牲生命也在所不惜。\n\n老国王去世后，约翰遵照遗愿带领新王参观宫殿，唯独没有打开那个特殊的房n为了帮助国王实现愿望，约翰提议用大量金银财宝作为礼物前往金屋国。他们装扮成商人出发，成功吸引了公主的兴趣。当公主登船欣赏珍宝时，船只已经悄然启航。起初，公主惊恐万分，但在得知对方也是国王且真心爱慕自己后最后一次则关于新娘的生命危险。尽管知晓这些预言，但为了避免国王冒险救人导致自身变成石头，约翰选择了沉默。\n\n回国后，预言一一应验。约翰每次都抢先一步化解危机，却因此被误解为背叛者而遭到囚禁。直到行刑前一刻子以换取约翰的生命），他们的信念和勇气也从未动摇。最终，所有挑战都被克服，故事以一个美满结局告终，展现了忠诚与真爱的力量。
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