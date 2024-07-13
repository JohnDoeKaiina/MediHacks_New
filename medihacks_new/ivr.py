import speech_recognition as sr


class AI_Assistant:
    def __init__(self):

        self.full_transcript = []  # Store full conversation transcript

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


# Example usage:
if __name__ == "__main__":

    # Continuously listen for speech input
    while True:
        ai_assistant.speech_to_text()
