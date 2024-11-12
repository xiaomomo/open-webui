import ocrmypdf
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
import io
import os
import subprocess

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





# if __name__ == "__main__":
#     input_file = "chinese_grade1_up.pdf"
#
#     if os.path.exists(input_file):
#         text_content = process_pdf(input_file)
#         print(text_content)
#
#     else:
#         print("输入文件不存在")

if __name__ == "__main__":
    text_content = extract_text_from_pdf("output_no_transparency_ocr.pdf")
    print(text_content)