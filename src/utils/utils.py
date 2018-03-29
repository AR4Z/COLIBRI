#from voxpopuli import Voice
#from gtts import gTTS
import re
import subprocess
import fitz

def text_to_audio(name_text,speed, name_audio, lang="es"):
    subprocess.call("espeak -v {0} -f text.txt -p 45 -s 150 -w foo.wav".format(lang), shell=True)

# def text_to_audio(text, speed, name_audio):
#     print(text, speed)
#     voice = Voice(lang="es", pitch=99, speed=speed, voice_id=1)
#     wavs = voice.to_audio(text)
#     path_audio = "/home/ar4z/Audiolibros/" + name_audio[:-4] + ".wav"
#     with open(path_audio, "wb") as wavfile:
#         wavfile.write(wavs)
#
#     return path_audio

# def text_to_audio(text, speed, name_audio):
#     print(text)
#     tts = gTTS(text=text, lang='es')
#     tts.save(name_audio[:-4]+ ".mp3")


def extract_text(path_pdf, from_page, until_page):
    doc = fitz.open(path_pdf)
    text = ""
    for number_page in range(from_page, until_page):
        page = doc.loadPage(number_page)
        text += page.getText("text")

    text.replace('\n', ' ')
    file = open("text.txt", 'w')
    file.write(text)
    file.close()
    return text

def extract_name_audio(path):
    pattern = re.compile(r"\w+(?:\.\w+)*$")
    return pattern.findall(path)[0]

print(extract_text("/home/ar4z/Downloads/Macroeconomia de Bernanke.PDF", 0, 28))