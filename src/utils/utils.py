from voxpopuli import Voice
import textract

def text_to_audio(text, speed):
    print(text, speed)
    voice = Voice(lang="es", pitch=99, speed=speed, voice_id=1)
    wavs = voice.to_audio(text)

    with open("/home/ar4z/Audiolibros/texto.wav", "wb") as wavfile:
        wavfile.write(wavs)

    return "/home/ar4z/Audiolibros/texto.wav"


def extract_text(path_pdf):
    text = textract.process(path_pdf)

    decode_text = text.decode('utf-8')

    decode_text.replace('\n', ' ')
    return decode_text
