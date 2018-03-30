import re
import subprocess
import fitz
import pydub
import os

def text_to_audio(speed, name_audio, pitch, lang="es"):
    subprocess.call("espeak -v {0} -f text.txt -p {1} -s {2} -w /home/ar4z/Audiolibros/{3}.wav".format(lang, pitch, speed, name_audio), shell=True)
    return wav_to_mp3("/home/ar4z/Audiolibros/{0}.wav".format(name_audio))


def extract_text(path_pdf, from_page, until_page):
    doc = fitz.open(path_pdf)
    text = ""
    if from_page != 0:
        from_page -= 1
    for number_page in range(from_page, until_page):
        page = doc.loadPage(number_page)
        text += page.getText("text")

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
