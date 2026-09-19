import speech_recognition as sr

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_thrshold = 2

        print("Speak Something...")
        audio = r.listen(source)

        print("Processing Audio... (STT)")
        stt = r.recognize_google(audio)

        print("You Said:", stt)

main()