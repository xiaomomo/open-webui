import ocrmypdf
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
import io
import os
import subprocess
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from open_webui.apps.englishlesson.workflows.struct_lesson.struct_lesson_content import StructLessonWorkflow
from open_webui.apps.webui.models.fredisalesson import FredisaLessonForm, FredisaLessonModel, FredisaLessons


import asyncio

def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager,
        fake_file_handle,
        laparams=LAParams(),
        codec='utf-8'
    )
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh):
            page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()

    return text

def process_pdf(input_path):
    try:
        # OCR 处理
        command = f'ocrmypdf {input_path} {input_path + "_ocr.pdf"} --force-ocr'
        subprocess.run(command, shell=True, check=True)
        # 使用改进的文本提取方法
        text = extract_text_from_pdf(input_path+'_ocr.pdf')
        return text

    except ocrmypdf.exceptions.PriorOcrFoundError:
        print("PDF已包含OCR文本层")
        return extract_text_from_pdf(input_path)
    except Exception as e:
        print(f"处理出错: {str(e)}")
        return None

async def save_unit(item):
    # 如果item长度小于50，直接返回
    if len(item) < 50:
        return
    # save item to sqlite
    fredisaLesson = FredisaLessonForm(unit=item.split('\n')[0], content=item, lesson_json="")
    fredisaLesson.content = item
    fredisaLesson.unit = item.split('\n')[0]
    # 调用工作流结构化lesson
    w = StructLessonWorkflow(timeout=40, verbose=False)
    lesson_json = await w.run(origin_content=fredisaLesson.content)
    print(lesson_json)
    fredisaLesson.lesson_json = lesson_json
    lesson = FredisaLessons.insert_new_lesson(fredisaLesson)
    # 调用工作流结构化 question
    time.sleep(1)
    return lesson



async def savePdfContent(text_content):
    # todo 这里要用更好的截取办法，去掉脏数据
    units = [unit.strip() for unit in text_content.split("Unit ") if unit.strip()]
    for item in units:
        await save_unit(item)


if __name__ == "__main__":
    input_file = "level5.pdf"

    if os.path.exists(input_file):
        text_content = process_pdf(input_file)
        if text_content:
            # 移除多余的空白行
            text_content = '\n'.join(line for line in text_content.splitlines() if line.strip())
            print("提取的文本内容:")
            print(text_content)
            asyncio.run(savePdfContent(text_content))

    else:
        print("输入文件不存在")