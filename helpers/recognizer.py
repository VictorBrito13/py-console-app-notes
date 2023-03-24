import speech_recognition as sr

class Recognizer():
    def __init__(self):
        self.audio = None
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.recognizer.pause_threshold = 2

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            self.audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)

    def recognize(self):
        print("\n speak...\n")
        self.listen()
        transcription = self.recognizer.recognize_google(self.audio)
        return transcription

