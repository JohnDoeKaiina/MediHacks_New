
class AIAssistant:
    def __init__(self):
        self.full_transcript = []

    def generate_ai_response(self, text):
        self.full_transcript.append({"role": "user", "content": text})
        print(f"Patient: {text}")
        ai_client = Groq()

        chat_completion = ai_client.chat.completions.create(

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
            stop=None,
            stream=False,
        )

        
        ai_response=chat_completion.choices[0].message.content

        print("ai_responseai_responseai_response",ai_response)
        return ai_response

