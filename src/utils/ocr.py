import sys
from pdf2image import convert_from_path
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]
langs = tool.get_available_languages()
lang = langs[1]


def ocr(path_pdf, from_page, until_page):
    images = convert_from_path(path_pdf, first_page=from_page, last_page=until_page)
    txt = ""
    for image in images:
        txt += tool.image_to_string(
            image,
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
    print(txt)
    return txt
