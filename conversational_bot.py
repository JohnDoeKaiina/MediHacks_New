import speech_recognition as sr
from elevenlabs import generate, stream
from groq import Groq
from PIL import Image, ImageDraw

import time
import sqlite3
from dotenv import load_dotenv
import os
import openai

load_dotenv()


class colors:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"  # End color sequence


color_mapping = {
    "happy": (255, 255, 0),  # Yellow
    "sad": (0, 0, 255),  # Blue
    "angry": (255, 0, 0),  # Red
    "neutral": (128, 128, 128),  # Gray
}


def generate_mood_map():
    conn = sqlite3.connect("db.sqlite3")
    dic = {}

    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_moodtracker")
            rows = cursor.fetchall()

            dic = {}
            for row in rows:
                emotions = row[
                    2
                ].lower()  # Assuming emotions are stored in lowercase in the database
                if emotions in dic:
                    dic[emotions] += 1
                else:
                    dic[emotions] = 1

            print(dic)

            # Generate an image representation
            image_size = (400, 200)
            image = Image.new("RGB", image_size, (255, 255, 255))  # White background
            draw = ImageDraw.Draw(image)

            # Draw rectangles representing each emotion count
            max_count = max(dic.values()) if dic else 1  # Avoid division by zero
            bar_width = image_size[0] / len(dic)

            x = 0
            for emotion, count in dic.items():
                color = color_mapping.get(
                    emotion, (0, 0, 0)
                )  # Default to black if no color mapping found
                bar_height = (count / max_count) * image_size[1]
                draw.rectangle(
                    [x, image_size[1] - bar_height, x + bar_width, image_size[1]],
                    fill=color,
                )
                x += bar_width

            image.save("moodtracker_image.png")
            print("Image generated successfully.")

        except Exception as e:
            print("Error executing SQL query:", e)
        finally:
            conn.close()

    # PROMPT = "Generate an abstract image with the following colors in the dictionary {dic}"
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # response = openai.Image.create(
    #     prompt=PROMPT,
    #     n=1,
    #     size="256x256",
    # )

    # print(response["data"][0]["url"])


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
            print(colors.PURPLE + colors.BOLD + "\n User: " + colors.END)
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
        if "generate my mood map" in text:
            generate_mood_map()
        else:
            client = Groq()

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "A person is going through a long recovery. You must act like its personal friend and cheering them. Also ask for daily mood updates.",
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
                model="llama3-8b-8192",
                temperature=0.2,
                max_tokens=5024,
                top_p=1,
                stop=None,
                stream=False,
            )
            ai_response = chat_completion.choices[0].message.content

            print(colors.GREEN + "\nAI Receptionist: " + colors.END)
            print(ai_response)
            self.generate_audio(ai_response)

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        audio_stream = generate(
            api_key=self.elevenlabs_api_key, text=text, voice="Rachel", stream=True
        )
        stream(audio_stream)


if __name__ == "__main__":
    print("\n\n\n")
    greeting="Hey there! How are you feeling today?"
    print(colors.GREEN + '\nAI Receptionist: ' + colors.END)
    print(greeting)
    ai_assistant = AI_Assistant()
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()

    # Continuously listen for speech input
    while True:
        ai_assistant.speech_to_text()
