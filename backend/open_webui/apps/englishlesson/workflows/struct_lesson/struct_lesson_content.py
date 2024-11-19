from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
)

from .schemas import *
from .prompts import *
import json
from dashscope import Generation



# workflow step:
#     1. start
#     2. struct content
#     3. review struct content
#     4. save content
#     5. finish

class StartJsonLessonEvent(Event):
    jsonUnitContent: str
    origin_content: str


class StartStructLessonEvent(Event):
    origin_content: str


class FinishStructLessonEvent(Event):
    lessonUnit: LessonUnit


class SaveStructLessonEvent(Event):
    lessonUnit: LessonUnit


class StructLessonWorkflow(Workflow):

    @step
    async def step_start(self, ev: StartEvent) -> StartStructLessonEvent:
        print(f"step_start response: {ev.origin_content}")
        return StartStructLessonEvent(origin_content=ev.origin_content)

    @step
    async def step_struct_content(self, ev: StartStructLessonEvent) -> StartJsonLessonEvent:
        prompt = f"{parse_lesson_content.format(content=ev.origin_content)}"
        response = Generation.call(
            model='qwen-max',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        responseText = response.output.text
        print(f"step_struct_content response: {responseText}")
        return StartJsonLessonEvent(jsonUnitContent=responseText, origin_content=ev.origin_content)

    @step
    async def step_json_content(self, ev: StartJsonLessonEvent) -> FinishStructLessonEvent | StartEvent:
        prompt = f"{json_lesson_content.format(content=ev.jsonUnitContent)}"
        response = Generation.call(
            model='qwen-max',
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        responseText = response.output.text
        print(f"step_struct_content response: {responseText}")
        try:
            lessonUnit = self.parse_lesson_unit(responseText)
            lessonUnit.origin_content=ev.origin_content
            print("success parse content json")
            return FinishStructLessonEvent(lessonUnit=lessonUnit)
        except:
            print("fail parse content json, repeat from start")
            ## 不能进start节点
            return StartStructLessonEvent(origin_content=ev.origin_content)


    @step
    async def step_review_struct_event(self,
                                       ev: FinishStructLessonEvent) -> StartJsonLessonEvent | SaveStructLessonEvent:
        # lesson_dict = ev.lessonUnit.to_dict()
        # origin_content = lesson_dict['origin_content']
        # lesson_dict.pop("origin_content", None)  # 移除 'origin_content' 属性
        # json_str = json.dumps(lesson_dict, indent=4)
        # prompt = f"{review_parse_lesson_content.format(origin_content=origin_content, content_json=json_str)}"
        # response = Generation.call(
        #     model='qwen-max',
        #     messages=[
        #         {'role': 'user', 'content': prompt}
        #     ]
        # )
        # responseText = response.output.text
        # print(f"step_review_struct_event input:{prompt} \n response: {responseText}")
        # if "true" in responseText:
        #     print("json content same as origin content")
        #     return SaveStructLessonEvent(lessonUnit=ev.lessonUnit)
        # else:
        #     print("json content not same as origin content, repeat from start")
        #     return StartEvent(origin_content=origin_content)
        return SaveStructLessonEvent(lessonUnit=ev.lessonUnit)

    @step
    async def step_save_content(self, ev: SaveStructLessonEvent) -> StopEvent:
        json_str = json.dumps(ev.lessonUnit.to_dict(), indent=4)
        print(f"step_save_content response: {json_str}")
        return StopEvent(result=json_str)


    def parse_lesson_unit(self, responseText: str) -> LessonUnit:
        try:
            # 尝试将响应文本解析为 JSON 对象
            data = json.loads(responseText)
            # 使用 LessonUnit 类的 from_dict 方法创建 LessonUnit 实例
            lessonUnit = LessonUnit.from_dict(data)
            return lessonUnit
        except json.JSONDecodeError as e:
            # 如果解析失败，抛出异常
            print(f"Invalid JSON: {e}")
            raise ValueError(f"Failed to parse JSON: {e}")
        except Exception as e:
            # 处理其他可能的异常
            print(f"Error occurred: {e}")
            raise ValueError(f"Failed to create LessonUnit: {e}")



async def main():
    origin_content = '''
    Unit I- Animal Comparisons
Objectives:
e Teach children how to compare animals using comparatives and superlatives. e The lesson also teaches English learners other ways of describing animals
using essential vocabulary.
The skills learned in this lesson will enable EFL/ESL young learners to be able to compare and contrast people, objects, animals and more. Learning comparisons in English is an essential communication skill every learner needs.
Lesson Story:
Mom, Dad, Freddie and Lisa are visiting the zoo. They are delighted to see swimming turtles and otters. This leads to a conversation on the differences between the animals in the zoo.
Vocabulary: Adjectives - Opposites
big small fast tall colorful
Comparing Animals big
small fast tall playful colorful
small large slow short plain
www.fredisalearns.com
bigger smaller
faster
taller
more playful more colorful
biggest smallest fastest tallest
most playful most colorful
1|Page
 Key Sentences:
Elephants are bigger than lions.
Elephants are the biggest animals in the zoo. The angelfish is smaller than a turtle.
. The angelfish is the smallest animal in the zoo. Giraffes are taller than zebras.
Giraffes are the tallest animals in the zoo. Otters swim faster than turtles.
Turtles swim slower than otters.
QAWEOWNONAN
.
The sailfish is the fastest swimmer in the world. lO.Monkeys are more playful than otters.
Il. Monkeys are the most playful animals in the zoo.
Comparing using ‘as’
|. Zebras are as big as horses.
2. The angelfish is as big as my thumb.
More ways to describe animals
|. Tigers and zebras have stripes.
2. Horses do not have stripes but zebras do. 3. A lion's roar sounds scary.
    '''
    w = StructLessonWorkflow(timeout=40, verbose=False)
    result = await w.run(origin_content=origin_content)
    print("1111111:"+result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
