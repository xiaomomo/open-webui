from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)

from prompts import *
from llama_index.llms.ollama import Ollama
import json

LESSON_JSON = "lesson_json"

llm = Ollama(model="llama3:8b", request_timeout=120.0)


# workflow step:
#     1. start
#     2. generate question
#     3. be json
#     4. save question

class StartGenerateQuestionEvent(Event):
    pass

class StartQuestionJsonEvent(Event):
    question_json: str

class CheckJsonEvent(Event):
    question_json: str


class SaveQuestionEvent(Event):
    question_json: str


class LessonQuestionWorkflow(Workflow):

    @step
    async def step_start(self, ctx: Context, ev: StartEvent) -> StartGenerateQuestionEvent:

        # load data
        await ctx.set("lesson_json", ev.origin_content)
        return StartGenerateQuestionEvent()

    @step
    async def step_generate_question(self, ctx: Context,ev: StartGenerateQuestionEvent) -> StartQuestionJsonEvent:
        lesson_json = await ctx.get(LESSON_JSON);
        prompt = f"{DESIGN_QUESTION.format(course_content=lesson_json)}"
        responseText = llm.complete(prompt).text
        print(f"step_generate_question response: {responseText}")
        return StartQuestionJsonEvent(question_json=responseText)

    @step
    async def step_parse_json_content(self, ev: StartQuestionJsonEvent) -> CheckJsonEvent:
        prompt = f"{STRUCT_QUESTION.format(question_json=ev.question_json)}"
        print(f"step_json_content prompt prompt prompt prompt: {prompt}")
        responseText = llm.complete(prompt).text
        print(f"step_struct_content response: {responseText}")
        return CheckJsonEvent(question_json=responseText)

    @step
    async def step_check_json_content(self, ev: CheckJsonEvent) -> SaveQuestionEvent | StartGenerateQuestionEvent:
        prompt = f"{JSON_LESSON_CONTENT.format(content=ev.question_json)}"
        responseText = llm.complete(prompt).text
        print(f"step_struct_content response: {responseText}")
        try:
            json.loads(responseText)
            print("success parse content json")
            return SaveQuestionEvent(question_json=responseText)
        except json.JSONDecodeError:
            print("fail parse content json, repeat from start")
            return StartGenerateQuestionEvent()

    @step
    async def step_save_question(self, ev: SaveQuestionEvent) -> StopEvent:
        print(f"step_save_question response: {ev.question_json}")
        return StopEvent(result="Workflow complete.")

async def main():
    origin_content = '''
    {
    "unit": "I- Animal Comparisons",
    "objectives": [
        "Teach children how to compare animals using comparatives and superlatives.",
        "The lesson also teaches English learners other ways of describing animals using essential vocabulary."
    ],
    "lesson_story": "Mom, Dad, Freddie and Lisa are visiting the zoo. They are delighted to see swimming turtles and otters. This leads to a conversation on the differences between the animals in the zoo.",
    "vocabulary": [
        "Adjectives - Opposites",
        "big",
        "small",
        "fast",
        "tall",
        "colorful",
        "bigger",
        "smaller",
        "faster",
        "taller",
        "more playful",
        "more colorful",
        "biggest",
        "smallest",
        "fastest",
        "tallest",
        "most playful",
        "most colorful"
    ],
    "key_sentences": [
        "Elephants are bigger than lions.",
        "Elephants are the biggest animals in the zoo.",
        "The angelfish is smaller than a turtle.",
        "The angelfish is the smallest animal in the zoo.",
        "Giraffes are taller than zebras.",
        "Giraffes are the tallest animals in the zoo.",
        "Otters swim faster than turtles.",
        "Turtles swim slower than otters.",
        "The sailfish is the fastest swimmer in the world.",
        "lO.Monkeys are more playful than otters.",
        "Il. Monkeys are the most playful animals in the zoo.",
        "Zebras are as big as horses.",
        "The angelfish is as big as my thumb.",
        "Tigers and zebras have stripes.",
        "Horses do not have stripes but zebras do.",
        "A lion's roar sounds scary."
    ]
}
    '''
    w = LessonQuestionWorkflow(timeout=40, verbose=False)
    result = await w.run(origin_content=origin_content)
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
