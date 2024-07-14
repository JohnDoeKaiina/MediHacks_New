import os
from groq import Groq
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask import Flask, request, render_template
from twilio.rest import Client

app = Flask(__name__)

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)



class AIAssistant:
    def __init__(self):
        self.full_transcript = []
        self.ai_client = Groq(
    api_key="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"
)
    def generate_ai_response(self, text):
        self.full_transcript.append({"role": "user", "content": text})
        print(f"Patient: {text}")

        chat_completion = self.ai_client.Completion.create(
            engine="davinci-codex",
            prompt=f"You: {text}\nAI:",
            max_tokens=150,
            stop=None,
        )

        ai_response = chat_completion.choices[0].text.strip()

        self.generate_audio(ai_response)
        return ai_response

    def generate_audio(self, response):
        # Implement audio generation logic here
        print(f"AI Response: {response}")

ai_assistant = AIAssistant()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/call", methods=['POST'])
def call():
    twilio_number = '+'
    target_number = '+'

    call = client.calls.create(
        to=target_number,
        from_=twilio_number,
        url='https://0abb-2401-4900-8839-1eb3-b16b-5c52-cc0c-833b.ngrok-free.app/voice'  # Replace with your actual Ngrok URL
    )
    return "Call initiated!", 200



@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb with speech recognition
    gather = Gather(input='speech', action='/gather')
    gather.say('He describe your emergency.')
    resp.append(gather)

    # If the user doesn't provide input, redirect them into a loop
    resp.redirect('/voice')

    return str(resp)


@app.route('/gather', methods=['POST'])
def gather():
    """Processes results from the user's speech input"""
    user_input = request.form['SpeechResult']
    ai_response = ai_assistant.generate_ai_response(user_input)

    resp = VoiceResponse()
    resp.say(ai_response)

    return str(resp)
if __name__ == "__main__":
    app.run(debug=True)