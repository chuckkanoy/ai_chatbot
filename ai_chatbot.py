import numpy as np
import speech_recognition as sr
import pyttsx3
import os
import datetime
import transformers

class ChatBot():
    def __init__(self, name):
        print("Booting up", name)
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            print("me --> ", self.text)
        except:
            print("me --> ERROR")
    
    def wake_up(self, text):
        return True if self.name.lower() in text.lower() else False

    @staticmethod
    def text_to_speech(text):
        print("AI --> ", text)
        converter = pyttsx3.init()
        converter.setProperty('rate', 150)
        converter.setProperty('volume', 1)
        # adjust based on male or female voice
        voice_id = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\'\
            'Tokens\\TTS_MS_EN-US_ZIRA_11.0'
        converter.setProperty('voice', voice_id)
        converter.say(text)
        converter.runAndWait()

    @staticmethod
    def action_time():
        return datetime.datetime.now().time().strftime('%H:%M')

if __name__ == "__main__":
    NAME = "Jarvis"
    ai = ChatBot(name=NAME)
    nlp = transformers.pipeline("conversational",
        model="microsoft/DialoGPT-medium")
    ex = True
    while ex:
        ai.speech_to_text()

        if ai.wake_up(ai.text) is True:
            res = "Hello I am {} the AI, what can I do for you?".format(NAME)
        elif 'time' in ai.text:
            res = ai.action_time()
        elif any(i in ai.text for i in ["thank", "thanks"]):
            res = np.random.choice(
                ["you're welcome!", "anytime!", "no problem!",
                "cool!", "I'm here if you need me!", "peace out!"]
            )
        elif any(i in ai.text for i in ["exit", "close", "goodbye"]):
            res = np.random.choice(["Have a good day", 
                "May your day bring you joy", "Goodbye"])
            ex = False
        else:
            if ai.text == "ERROR":
                res = np.random.choice([
                    "Could you repeat that?", "Sorry, I didn't get that",
                    "What was that?"
                ])
            else:
                chat = nlp(transformers.Conversation(ai.text), 
                    pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ")+6:].strip()
        os.system("cls")
        
        ai.text_to_speech(res)