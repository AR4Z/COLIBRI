try:
    import Image
except ImportError:
    from PIL import Image

from pdf2image import convert_from_path
import subprocess
import platform
import pytesseract
import os
from pathlib import Path
import zipfile

if platform.system() == "Windows":
    if not os.path.exists("C:\\Program Files (x86)\\Tesseract-OCR"):
        p = subprocess.Popen([r"bin/tessereact.exe"])
        p_status = p.wait()

    if not os.path.exists("{0}".format(os.path.join(Path.home(), "bin", "poppler-0.51"))):
            with zipfile.ZipFile("poppler-0.51.zip", "r") as zip_ref:
                zip_ref.extractall(os.path.join(Path.home(), "bin", "poppler-0.51\\"))

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


def ocr(path_pdf, from_page, until_page):
    images = convert_from_path(path_pdf, first_page=from_page, last_page=until_page)
    txt = ""
    for image in images:
        txt += pytesseract.image_to_string(image,
            lang='spa'
        )
    print(txt)
    return txt
