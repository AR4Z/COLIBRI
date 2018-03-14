from voxpopuli import Voice
import textract, re

def text_to_audio(text, speed, name_audio):
    print(text, speed)
    voice = Voice(lang="es", pitch=99, speed=speed, voice_id=1)
    wavs = voice.to_audio(text)
    path_audio = "/home/ar4z/Audiolibros/" + name_audio[:-4] + ".wav"
    with open(path_audio, "wb") as wavfile:
        wavfile.write(wavs)

    return path_audio


def extract_text(path_pdf):
    text = textract.process(path_pdf)

    decode_text = text.decode('utf-8')

    decode_text.replace('\n', ' ')
    return decode_text

def extract_name_audio(path):
    pattern = re.compile(r"\w+(?:\.\w+)*$")
    return pattern.findall(path)[0]
