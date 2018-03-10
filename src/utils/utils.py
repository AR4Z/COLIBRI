from voxpopuli import Voice

def text_to_audio(dir_text, speed):
    print(dir_text, speed)
    voice = Voice(lang="es", pitch=99, speed=speed, voice_id=1)
    wav = voice.to_audio(dir_text)

    with open("texto.wav", "wb") as wavfile:
        wavfile.write(wav)

