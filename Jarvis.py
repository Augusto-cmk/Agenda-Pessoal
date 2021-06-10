import pyttsx3
import speech_recognition as speech

motor = pyttsx3.init()

def Falar(texto):
    motor.say(texto)
    motor.runAndWait()

def Ouvir():
    reconhecer = speech.Recognizer()
    try:
        with speech.Microphone() as microfone:
            Falar('Diga o comando que deseja')
            audio = reconhecer.listen(microfone)
            texto = reconhecer.recognize_google(audio,language='pt-BR')
            return texto.lower()
    except:
        pass
