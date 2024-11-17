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

# Create logger instance
logger = logging.getLogger(__name__)


class GenerateScreenplayEvent(Event):
    content: str

class ReviewScreenplayEvent(Event):
    screenplay: str
    original_content: str

class GenerateSceneImageEvent(Event):
    screenplay: str
    scene_description: str

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
    async def step_review_screenplay(self, ev: ReviewScreenplayEvent) -> Union[GenerateSceneImageEvent, GenerateScreenplayEvent]:
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
                return GenerateSceneImageEvent(
                    screenplay=ev.screenplay,
                    scene_description=ev.screenplay
                )
            print("Screenplay needs revision, generating new version")
            return GenerateScreenplayEvent(content=ev.original_content)
        except Exception as e:
            logger.error("Failed to review screenplay: %s", str(e))
            raise

    @step
    async def step_generate_scene_img(self, ev: GenerateSceneImageEvent) -> StopEvent:
        print("Generating scene images")
        prompt = prompt_generate_scene_img.format(
            screenplay=ev.screenplay,
            scene_description=ev.scene_description
        )
        try:
            image_result = llm.complete(prompt).text
            print("Successfully generated scene images")
            print("Image generation result: %s", image_result)
            
            final_result = {
                "screenplay": ev.screenplay,
                "scene_images": image_result
            }
            return StopEvent(result=json.dumps("finished"))
        except Exception as e:
            logger.error("Failed to generate scene images: %s", str(e))
            raise

async def main():
    print("Starting main workflow execution")
    # Test content
    test_content = """
马棚里住着一匹老马和一匹小马。

有一天，老马对小马说：“你已经长大了，能帮妈妈做点事吗？”小马连蹦带跳地说：“怎么不能？我很愿意帮您做事。”老马高兴地说：“那好啊，你把这半口袋麦子驮到磨坊去吧。”

小马驮起口袋，飞快地往磨坊跑去。跑着跑着，一条小河挡住了去路，河水哗哗地流着。小马为难了，心想：我能不能过去呢？如果妈妈在身边，问问她该怎么办，那多好啊！可是离家很远了。小马向四周望望，看见一头老牛在河边吃草，小马“嗒嗒嗒”跑过去，问道：“牛伯伯，请您告诉我，这条河，我能趟过去吗？”老牛说：“水很浅，刚没小腿，能趟过去。”

小马听了老牛的话，立刻跑到河边，准备过去。突然，从树上跳下一只松鼠，拦住他大叫：“小马！别过河，别过河，你会淹死的！”小马吃惊地问：“水很深吗？”松鼠认真地说：“深的很哩！昨天，我的一个伙伴就是掉在这条河里淹死的！”小马连忙收住脚步，不知道怎么办才好。他叹了口气说：“唉！还是回家问问妈妈吧！”

小马甩甩尾巴，跑回家去。妈妈问他：“怎么回来啦？”小马难为情地说：“一条河挡住了去路，我……我过不去。”妈妈说：“那条河不是很浅吗？”小马说：“是呀！牛伯伯也这么说。可是松鼠说河水很深，还淹死过他的伙伴呢！”妈妈说：“那么河水到底是深还是浅呢？你仔细想过他们的话吗？”小马低下了头，说：“没……没想过。”妈妈亲切地对小马说：“孩子，光听别人说，自己不动脑筋，不去试试，是不行的，河水是深是浅，你去试一试，就知道了。”

小马跑到河边，刚刚抬起前蹄，松鼠又大叫起来：“怎么？你不要命啦！？”小马说：“让我试试吧！”他下了河，小心地趟到了对岸。

原来河水既不像老牛说的那样浅，也不像松鼠说的很深。
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
        
    except Exception as e:
        logger.error("Workflow failed: %s", str(e))
        raise

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
