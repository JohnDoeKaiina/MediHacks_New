import os
from groq import Groq
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask import Flask, request, render_template
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)



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
                    "content": "You are a AI 911 operator. When user ask them a question, first calm them down. Then send help and provide first aid suggestions"
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



ai_assistant = AIAssistant()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/call", methods=['POST'])
def call():
    twilio_number = os.getenv("TWILIO_NUMBER")
    target_number = os.getenv("TWILIO_DESTINATION_NUMBER")

    call = client.calls.create(
        to=target_number,
        from_=twilio_number,
        url='https://db08-223-185-135-133.ngrok-free.app/voice'  # Replace with your actual Ngrok URL
    )
  
    return "Call initiated!", 200


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    if request.method == 'POST':
        # Check if 'SpeechResult' is in the form data
        if 'SpeechResult' in request.form:
            user_input = request.form['SpeechResult']
            ai_response = ai_assistant.generate_ai_response(user_input)
            resp.say(ai_response)
        else:
            # If 'SpeechResult' is not present, re-prompt for input
            gather = Gather(input='speech', action='/gather')
            gather.say('Please describe your emergency.')
            resp.append(gather)
            resp.redirect('/voice')  # Redirect to handle no input scenario
    else:
        # Initial prompt for speech input
        gather = Gather(input='speech', action='/gather')
        gather.say('Please describe your emergency.')
        resp.append(gather)
        resp.redirect('/voice')  # Redirect to handle no input scenario

    return str(resp)  # Ensure a valid response is returned

@app.route('/gather', methods=['POST'])
def gather():
    """Processes results from the user's speech input"""
    user_input = request.form['SpeechResult']
    ai_response = ai_assistant.generate_ai_response(user_input)

    resp = VoiceResponse()
    resp.say(ai_response)

    # Continue gathering input after responding
    gather = Gather(input='speech', action='/gather')
    gather.say('Please describe your emergency.')
    resp.append(gather)
    resp.redirect('/voice')  # Redirect to handle no input scenario

    return str(resp)  # Ensure a valid response is returned

if __name__ == "__main__":
    app.run(debug=True)