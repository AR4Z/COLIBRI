import re
import subprocess
import fitz
import os
import platform
import errno
import zipfile
# from .ocr import ocr
from pathlib import Path
from mutagen.mp3 import MP3
if platform.system() == "Windows":
    import winreg as reg
    import win32gui
    import win32con


def text_to_audio(speed, name_audio, pitch, path, lang="es"):
    name_audio = clean(name_audio)
    
    if platform.system() == "Windows":
        cmd = "\"C:\Program Files (x86)\eSpeak\command_line\espeak\" -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(
                lang, pitch, speed, path, name_audio)
    else:
        cmd = "espeak -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(lang, pitch, speed, path, name_audio) 

    if not os.path.exists("C:\\Program Files (x86)\\eSpeak\\command_line"):
        p = subprocess.Popen([r"bin/espeak-tts.exe"])
        (output, err) = p.communicate()
        p_status = p.wait()
        subprocess.call(cmd, shell=True)                      
    else:
        subprocess.call(cmd, shell=True)

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
    # else:
    # text = ocr(path_pdf, from_page, until_page)

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

    if platform.system() == "Windows":
        cmd = '{0}\\lame --preset insane {1}'.format(os.path.join(Path.home(), "bin", "lame"), path_wav)
    else:
        cmd = "lame --preset insane {0}".format(path_wav)

    if not os.path.exists("{0}\\lame".format(os.path.join(Path.home(), "bin", "lame"))):
        with zipfile.ZipFile("lame.zip", "r") as zip_ref:
            zip_ref.extractall(os.path.join(Path.home(), "bin", "lame\\"))
    subprocess.call(cmd, shell=True)         

    os.remove(path_wav)
    return path_wav[:-4] + ".mp3"


def len_audio_file(path_audio_file):
    audio = MP3(path_audio_file)
    return audio.info.length


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
        data = count_file.read()

    return data


def secondOnce():
    with open('count.txt', 'w') as count_file:
        data = count_file.write("1")
