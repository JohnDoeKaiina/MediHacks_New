import speech_recognition as sr
from elevenlabs import generate, stream
from groq import Groq


# from dotenv import load_dotenv
import os

# Load environment variables from .env file
# load_dotenv()

class AI_Assistant:
    def __init__(self):
        self.elevenlabs_api_key = ""

        self.full_transcript = []  

    def start_transcription(self):
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()

    def stop_transcription(self):
        pass  # No need to stop anything for speech_recognition

    def speech_to_text(self):
        with sr.Microphone() as source:
            print("Say something...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            self.generate_ai_response(text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Speech Recognition service; {e}")

    def generate_ai_response(self, text):
        self.full_transcript.append({"role": "user", "content": text})
        print(f"Patient: {text}")

        
        client = Groq()

        chat_completion = client.chat.completions.create(

            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistant."
                },

                {
                    "role": "user",
                    "content": text,
                }
            ],


            model="llama3-8b-8192",
            temperature=0.2,
            max_tokens=5024,
            top_p=1,

            # A stop sequence is a predefined or user-specified text string that
            # signals an AI to stop generating content, Examples "[end]".
            stop=None,
            stream=False,
        )

        
        ai_response=chat_completion.choices[0].message.content


        self.generate_audio(ai_response)

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"AI Receptionist: {text}")

        audio_stream = generate(
            api_key=self.elevenlabs_api_key,
            text=text,
            voice="Rachel",
            stream=True
        )
        stream(audio_stream)

if __name__ == "__main__":
    greeting = "listen?"
    ai_assistant = AI_Assistant()
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()

    # Continuously listen for speech input
    while True:
        ai_assistant.speech_to_text()

print(db_host)