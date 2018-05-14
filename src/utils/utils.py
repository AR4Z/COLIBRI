import re
import subprocess
import fitz
import os
import platform
import errno
import zipfile
from .ocr import ocr
from pathlib import Path
from mutagen.mp3 import MP3
from gtts import gTTS


def text_to_audio(speed, name_audio, pitch, path, tts, lang="es"):
    name_audio = clean(name_audio)
    
    if platform.system() == "Windows":
        cmd = "\"C:\Program Files (x86)\eSpeak\command_line\espeak\" -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(
                lang, pitch, speed, path, name_audio)

        if not os.path.exists("C:\\Program Files (x86)\\eSpeak\\command_line"):
            p = subprocess.Popen([r"bin/espeak-tts.exe"])
            p_status = p.wait()
            subprocess.call(cmd, shell=True)
    else:
        cmd = "espeak -v {0} -f text.txt -p {1} -s {2} -w {3}/{4}.wav".format(lang, pitch, speed, path, name_audio) 

    if tts == "espeak":
        subprocess.call(cmd, shell=True)
        return wav_to_mp3(os.path.join(path, name_audio + ".wav"))
    else:
        path_mp3 = os.path.join(path, name_audio + ".mp3")
        content = Path('text.txt').read_text()
        audio_tts = gTTS(content, slow=0, lang='es')
        audio_tts.save(path_mp3)
        velocity_human(path_mp3, speed)
        return path_mp3


def extract_text(path_pdf, from_page, until_page, mode_extract_text):
    if mode_extract_text == "pymupdf":
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
    text = text.replace('  ', ' ')
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

        if not os.path.exists("{0}\\lame".format(os.path.join(Path.home(), "bin", "lame"))):
            with zipfile.ZipFile("lame.zip", "r") as zip_ref:
                zip_ref.extractall(os.path.join(Path.home(), "bin", "lame\\"))
    else:
        cmd = "lame --preset insane {0}".format(path_wav)

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


def velocity_human(path_audio_mp3, speed):

    name_audio = extract_name_audio(path_audio_mp3)
    if platform.system() == "Windows":
        cmd = '\"C:\Program Files (x86)\sox-14-4-2\sox\" --show-progress {0} {1}\\output.mp3 tempo {2}'.format(path_audio_mp3,
                                                                                                               os.path.join(Path.home(),
                                                                                                           "AudioLibros"), speed)
        if not os.path.exists("C:\Program Files (x86)\sox-14-4-2"):
            p = subprocess.Popen([r"bin/sox-14.4.2-win32.exe"])
            p_status = p.wait()
            subprocess.call(cmd, shell=True)
    else:
        cmd = "sox --show-progress {0} {1}/output.mp3 tempo {2}".format(path_audio_mp3, os.path.join(Path.home(), "AudioLibros"), speed)

    subprocess.call(cmd, shell=True)

    os.remove(path_audio_mp3)
    os.rename(os.path.join(Path.home(), "AudioLibros", "output.mp3"), os.path.join(Path.home(), "AudioLibros", "{0}.mp3".format(name_audio)))


