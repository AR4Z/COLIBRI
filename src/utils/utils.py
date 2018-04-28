import re
import subprocess
import fitz
import pydub
import os
import platform
import errno
from .ocr import ocr


def text_to_audio(speed, name_audio, pitch, path, lang="es"):
    name_audio = clean(name_audio)
    if platform.system() == "Windows":
        subprocess.call(
            "\"C:\Program Files (x86)\eSpeak\command_line\espeak\" -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(lang, pitch, speed, path, name_audio),
            shell=True)
    else:
        subprocess.call(
            "espeak -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(lang, pitch, speed, path, name_audio),
            shell=True)

    return wav_to_mp3(os.path.join(path, name_audio + ".wav"))


def extract_text(path_pdf, from_page, until_page, mode):
    if mode == "pymupdf":
        doc = fitz.open(path_pdf)
        text = ""

        if from_page != 0:
            from_page -= 1

        for number_page in range(from_page, until_page):
            page = doc.loadPage(number_page)
            text += page.getText("text")
    else:
        text = ocr(path_pdf, from_page, until_page)

    print(text)
    text.replace('\n', ' ')
    file = open("text.txt", 'w', encoding='utf8')
    file.write(text)
    file.close()
    return text


def extract_name_audio(path):
    pattern = re.compile(r"(.+?)(?:\.[^.]*$|$)")
    return pattern.findall(path)[0].split("/")[-1]


def len_file_pdf(path_pdf):
    doc = fitz.open(path_pdf)
    return doc.pageCount


def wav_to_mp3(path_wav):
    cmd = 'lame --preset insane {0}'.format(path_wav)
    subprocess.call(cmd, shell=True)
    os.remove(path_wav)
    return path_wav[:-4] + ".mp3"


def len_audio_file(path_audio_file):
    sound = pydub.AudioSegment.from_mp3(path_audio_file)
    return sound.duration_seconds


def seconds_in_time_for_humans(seconds):
    hours = int(seconds / 3600)
    seconds %= 3600
    minutes = int(seconds / 60)
    seconds %= 60
    return "{0}:{1}:{2}".format(hours, minutes, int(seconds))


def create_directory(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def clean(string):
    return ''.join(ch for ch in string if ch.isalnum())


def firstOnce():
    with open('count.txt', 'r') as count_file:
        data=count_file.read()

    return data


def secondOnce():
    with open('count.txt', 'w') as count_file:
        data=count_file.write("1")
