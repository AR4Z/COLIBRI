import re
import subprocess
import fitz
import pydub
import os
import platform
import errno
from .ocr import ocr


def text_to_audio(speed, name_audio, pitch, path, lang="es"):
    if platform.system() == "Windows":
        subprocess.call(
            "\"C:\Program Files (x86)\eSpeak\command_line\espeak\" -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(lang, pitch, speed, path, name_audio),
            shell=True)
    else:
        subprocess.call(
            "espeak -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(lang, pitch, speed, path, name_audio),
            shell=True)

    name_audio = clean(name_audio)
    return wav_to_mp3("{0}/{1}.wav".format(path, name_audio))


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


def wav_to_mp3(path_wav):
    sound = pydub.AudioSegment.from_wav(path_wav)
    path_mp3 = path_wav[:-4] + ".mp3"
    sound.export(path_mp3, format="mp3")
    os.remove(path_wav)

    return path_mp3


def len_audio_file(path_audio_file):
    sound = pydub.AudioSegment.from_mp3(path_audio_file)
    return sound.duration_seconds


def seconds_in_time_for_humans(seconds):
    hours = int(seconds / 3600)
    seconds %= 3600
    minutes = int(seconds / 60)
    seconds %= 60
    return "{0}:{1}:{2}".format(hours, minutes, seconds)


def create_directory(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def clean(string):
    return ''.join(ch for ch in string if ch.isalnum())
