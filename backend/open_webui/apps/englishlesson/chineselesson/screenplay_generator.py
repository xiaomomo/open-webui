import os
import sys
import requests
from urllib.parse import urlparse
import json
import asyncio

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../../../'))
sys.path.append(project_root)

# Now import the modules
from open_webui.apps.englishlesson.chineselesson.workflows.chineselesson.screenplay_workflow import ScreenplayWorkflow
from open_webui.apps.englishlesson.chineselesson.workflows.chineselesson.screenplay_overview_image_workflow import ScreenplayImageWorkflow
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessons


def saveImageToStatic(screenplayImageUrl):
    # Define the static folder path
    static_folder = "/Users/liuqingjie/code/ai-tts/open-webui/static/static/screenplay_resource/"
    
    # Create the directory if it doesn't exist
    os.makedirs(static_folder, exist_ok=True)
    
    try:
        # Get the filename from the URL
        parsed_url = urlparse(screenplayImageUrl)
        filename = os.path.basename(parsed_url.path)
        
        # If filename is empty or has no extension, generate a default one
        if not filename or '.' not in filename:
            filename = f"screenplay_{hash(screenplayImageUrl)}.png"
        
        # Full path where the image will be saved
        save_path = os.path.join(static_folder, filename)
        
        # Download and save the image
        response = requests.get(screenplayImageUrl, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        # Return the relative path that can be used in the frontend
        return f"/static/screenplay_resource/{filename}"
    
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None


async def save_unit(item):

    # 调用工作流结构化screenplay
    w = ScreenplayWorkflow(timeout=600, verbose=False)
    print(f"workflow start with content:{item}")
    screenplay = await w.run(origin_content=item)

    # 调用工作流生成图片
    w = ScreenplayImageWorkflow(timeout=600, verbose=False)
    screenplayImage = await w.run(origin_content=item)
    # save it to static folder
    screenplayImagePath = saveImageToStatic(screenplayImage)
    print(f"workflow generate question_json:{screenplayImage}")

    # save item to sqlite
    fredisaLesson = FredisaLessonForm(
        unit=screenplay.title,
        subject="Chinese",  # Add default subject
        content=item,
        lesson_json=screenplay,
        question_json="",
        lesson_img=screenplayImagePath
    )
    lesson = FredisaLessons.insert_new_lesson(fredisaLesson)
    return lesson


if __name__ == "__main__":
    async def process_all_stories():
        try:
            # Read the JSON file
            with open('./grimm_stories_v2.json', 'r', encoding='utf-8') as file:
                stories = json.load(file)

            # Process each story
            for index, story in enumerate(stories):
                print(f"Processing story {index + 1}/{len(stories)}")
                try:
                    await save_unit(story['content'])
                    print(f"Successfully processed story {index + 1}")
                except Exception as e:
                    print(f"Error processing story {index + 1}: {str(e)}")
                    continue

            print("All stories have been processed")

        except FileNotFoundError:
            print("Error: grimm_stories_v2.json file not found in current directory")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in grimm_stories_v2.json")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

    # Run the async function
    asyncio.run(process_all_stories())

