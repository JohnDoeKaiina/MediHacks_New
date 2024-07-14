import speech_recognition as sr
from elevenlabs import generate, stream
from groq import Groq


import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()


class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'  # End color sequence


# Replace 'path_to_your_db' with the actual path to your db.sqlite3 file
conn = sqlite3.connect('db.sqlite3')


class AI_Assistant:
    def __init__(self):
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")

        self.full_transcript = []  

    def start_transcription(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

    def stop_transcription(self):
        pass 

    def speech_to_text(self):
        with sr.Microphone() as source:
            print(colors.PURPLE + colors.BOLD  + '\n User: ' + colors.END)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"{text}")
            self.generate_ai_response(text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Speech Recognition service; {e}")

    def generate_ai_response(self, text):
        self.full_transcript.append({"role": "user", "content": text})

        # client = Groq()

        # chat_completion = client.chat.completions.create(

        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "you are a helpful assistant."
        #         },

        #         {
        #             "role": "user",
        #             "content": text,
        #         }
        #     ],


        #     model="llama3-8b-8192",
        #     temperature=0.2,
        #     max_tokens=5024,
        #     top_p=1,

        #     # A stop sequence is a predefined or user-specified text string that
        #     # signals an AI to stop generating content, Examples "[end]".
        #     stop=None,
        #     stream=False,
        # )

        
        ai_response="fsdfsd"

        print(colors.GREEN + '\nAI Receptionist: ' + colors.END)
        print(ai_response)
        self.generate_audio(ai_response)

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})


        # audio_stream = generate(
        #     api_key=self.elevenlabs_api_key,
        #     text=text,
        #     voice="Rachel",
        #     stream=True
        # )
        # stream(audio_stream)

if __name__ == "__main__":
    greeting = "listen?"
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_user')

    # Fetch all rows
    rows = cursor.fetchall()

    # Display the rows
    for row in rows:
        print(row)
    ai_assistant = AI_Assistant()
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()

    # Continuously listen for speech input
    while True:
        ai_assistant.speech_to_text()

