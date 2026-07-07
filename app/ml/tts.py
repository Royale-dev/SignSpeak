"""
tts.py

Simple Text-to-Speech module for SignSpeak.
"""

import pyttsx3


class TextToSpeech:
    def __init__(self):
        self.rate = 170

    def speak(self, text: str):
        text = text.strip()

        if not text:
            return

        # Create a fresh engine every time.
        engine = pyttsx3.init()

        engine.setProperty("rate", self.rate)

        engine.say(text)
        engine.runAndWait()

        engine.stop()

        del engine