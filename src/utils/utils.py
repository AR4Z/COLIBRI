import re
import subprocess
import fitz


def text_to_audio(speed, name_audio, pitch, lang="es"):
    subprocess.call("espeak -v {0} -f text.txt -p {1} -s {2} -w /home/ar4z/Audiolibros/{3}.wav".format(lang, pitch, speed, name_audio), shell=True)
    return "/home/ar4z/Audiolibros/{0}.wav".format(name_audio)


def extract_text(path_pdf, from_page, until_page):
    doc = fitz.open(path_pdf)
    text = ""
    for number_page in range(from_page-1, until_page):
        page = doc.loadPage(number_page)
        text += page.getText("text")

    text.replace('\n', ' ')
    file = open("text.txt", 'w')
    file.write(text)
    file.close()
    return text


def extract_name_audio(path):
    pattern = re.compile(r"(.+?)(?:\.[^.]*$|$)")
    return pattern.findall(path)[0].split("/")[-1]


def len_file_pdf(path_pdf):
    doc = fitz.open(path_pdf)
    return doc.pageCount
