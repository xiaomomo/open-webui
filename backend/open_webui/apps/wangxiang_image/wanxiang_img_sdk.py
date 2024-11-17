from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import io
import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessonModel, FredisaLessons


def simple_call(prompt):
    rsp = ImageSynthesis.call(model=ImageSynthesis.Models.wanx_v1,
                              prompt=prompt,
                              n=1,
                              size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
        # save file to current directory
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


def append_lesson_img(lesson):
    prompt = lesson.lesson_json
    # prompt = '''
    #     "lesson_story": "Mom, Dad, Freddie and Lisa are visiting the zoo. They are delighted to see swimming turtles and otters. This leads to a conversation on the differences between the animals in the zoo.",
    #         "vocabulary": [
    #             "Adjectives - Opposites",
    #             "big",
    #             "small",
    #             "fast",
    #             "tall",
    #             "colorful",
    #         ],
    #
    #     This is my course content. Please draw a picture for my course theme. Add some My Little Pony elements.
    # '''
    # simple_call(prompt)
    # print(prompt)
    lessonForm = FredisaLessonForm(unit=lesson.unit, content=lesson.content,
                                   lesson_json=lesson.lesson_json, question_json=lesson.question_json,lesson_img="imgName")
    FredisaLessons.update_lesson_by_id(lesson.id,lessonForm)


if __name__ == '__main__':
    # todo
    # all_lessons = FredisaLessons.get_all_lessons()
    # for lesson in all_lessons:
    #     append_lesson_img(lesson)

    prompt = """
    Generate detailed scene image descriptions based on the following screenplay scene:

<screen>
{
            "sceneNumber": 3,
            "location": "马棚",
            "timeOfDay": "中午",
            "screenContent": "小马回到了马棚，老马正坐在那里休息。马棚里依旧温暖而宁静。",
            "playerBehavior": {
                "dialogue": [
                    {
                        "character": "老马",
                        "chinese": "怎么回来啦？"
                    },
                    {
                        "character": "小马",
                        "chinese": "一条河挡住了去路，我过不去。"
                    },
                    {
                        "character": "老马",
                        "chinese": "那条河不是很浅吗？"
                    },
                    {
                        "character": "小马",
                        "chinese": "是呀！牛伯伯也这么说。可是松鼠说河水很深，还淹死过他的伙伴呢！"
                    },
                    {
                        "character": "老马",
                        "chinese": "那么河水到底是深还是浅呢？你仔细想过他们的话吗？"
                    },
                    {
                        "character": "小马",
                        "chinese": "没...没想过。"
                    },
                    {
                        "character": "老马",
                        "chinese": "孩子，光听别人说，自己不动脑筋，不去试试，是不行的。河水是深是浅，你去试一试，就知道了。"
                    }
                ],
                "actions": "小马低下了头，显得有些羞愧。老马则用温柔的眼神看着他。"
            }
</screen>

Please create visual descriptions for each scene that include:

1. Setting Elements:
   - Physical environment and layout
   - Time of day and lighting
   - Props and relevant objects
   - Cultural-specific details

2. Character Visualization:
   - Character positions and poses
   - Detailed facial expressions showing emotional states
   - Natural gestures and body language
   - Culturally appropriate clothing and accessories
   - Personal style and character-specific details

3. Action Representation:
   - Dynamic movement and natural interactions
   - Emotional undertones in body language
   - Key moments in the dialogue with emotional weight
   - Visual cues for language learning
   - Environmental interaction details

4. Atmospheric Elements:
   - Lighting and shadows
   - Weather effects and time of day
   - Ambient details (people in background, street noise, etc.)
   - Mood-setting elements
    """
    simple_call(prompt)

