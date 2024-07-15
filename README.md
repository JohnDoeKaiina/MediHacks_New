## Inspiration
Every year, approximately 10 million people worldwide die due to delayed or inadequate emergency medical care. This staggering number highlights the urgent need for innovative solutions to improve the efficiency and effectiveness of emergency responses. Safeline aims to drastically reduce this figure by leveraging advanced technology to provide immediate assistance during emergencies.


## What it does
Safeline's comprehensive system is designed to provide rapid support during critical moments, ensuring timely medical intervention and effective communication with emergency contacts and healthcare providers. 

**It works in 3 phases**
### a.  Phase 1: Before an Accident
Safeline guides users through creating a detailed medical profile and emergency contact
### b.  Phase 2: During an Accident
- **AI Assistant 911 Operator Help**
    - **AI-powered virtual assistant** acts as a preliminary 911 operator.
    - Provides immediate medical advice, CPR instructions, and critical support.
- **One-Click Emergency Notification**
    - Sends an **instant alert to emergency contacts** with the user’s location and medical info.
    - Ensures timely help from loved ones.
- **Unique QR Code Generation**
    - **Scannable unique QR code** containing the user’s medical profile.
    - Easily accessible by medical professionals and emergency responders.
### c.  Phase 3: After an Accident
- Daily Medicine Reminders
    - Customized reminders for daily medication intake.
- AI Companionship During Recovery
    - Tracks progress and offers personalized support during recovery.
 
      
## Get started
1. Install the all the required dependencies 
```
pip install -r requirements.txt
```


2. Generate API tokens for
- twilio:- https://console.twilio.com/
  
![image](https://github.com/user-attachments/assets/b639f5b0-045c-45d3-b384-4e0a91c4b84d)

  - elevenslab:- https://elevenlabs.io/app/speech-synthesis
    ![image](https://github.com/user-attachments/assets/171df3d4-08ae-49c1-ab89-621a4ec0a591)

- Groq:- https://console.groq.com/keys
![image](https://github.com/user-attachments/assets/23eefde0-1beb-4d1e-8fa0-8b0446ca5779)

  
- DalleE- https://openai.com/index/dall-e-3/

3. Add all the tokens in .env file
```
GROQ_API_KEY=
ELEVENLABS_API_KEY=
OPEN_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_NUMBER=
TWILIO_DESTINATION_NUMBER=
```

4. Once that is done, then we need to update the db
```
python manage.py makemigrations
python manage.py migrate
```

5. To start the server, run the following
```
python manage.py runserver
```
This will start the website at http://127.0.0.1:8000

**Go to  http://127.0.0.1:8000/register to create a new user**

6. AI assistant is running as a flask app. TO trigger it, run
```
python twl_working.py
```
This will start the website at http://127.0.0.1:5000

- We need a callback url for interactive voice response in twilio. I had used ngrok for this
  https://dashboard.ngrok.com/get-started/setup 


