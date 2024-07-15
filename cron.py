

from datetime import datetime, time
import sched
import time
import sqlite3
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

def send_twilio_message(info):
        print("Sending a remainder message from twilio")
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)
        twilio_phone_number = os.getenv("TWILIO_NUMBER")
        phone_number =  os.getenv("TWILIO_DESTINATION_NUMBER")

        # Set up Twilio client
        client = Client(account_sid, auth_token)
        msg =f'This is a reminder to take your medicine- {info[3]}. The quantity is {info[4]} and it must be taken at {info[6]} for {info[5]} days'
        print(msg)
        # Attempt to send the message
        message = client.messages.create(
            body=msg,
            from_=twilio_phone_number,
            to=phone_number
        )

def check_medicion_schedule():
    conn = sqlite3.connect('db.sqlite3')
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_prescrition')
            rows = cursor.fetchall()
            
            current_time = datetime.now().time() 
            
            for row in rows:   
                # Parse medicion_time_str into a datetime.time object
                medicion_time_str = row[6]
                medicine_status=row[7]
                medicion_time = datetime.strptime(medicion_time_str, "%H:%M").time()

                # Now you can compare current_time with medicion_time
                if medicine_status=="Ongoing":
                    
                    if current_time.hour == medicion_time.hour and current_time.minute == medicion_time.minute:
                        print(f"Current time {current_time} matches medicion_time {medicion_time} in row: {row}")
                        send_twilio_message(row)

                    else:
                        print(f"Current time {current_time} does not match medicion_time {medicion_time} in row: {row}")
        except Exception as e:
            print("Error executing SQL query:", e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Database connection not established.")


scheduler = sched.scheduler(time.time, time.sleep)


def periodic_check(sc):
    check_medicion_schedule()
    # Reschedule the check every 1 minute (adjust as needed)
    scheduler.enter(60, 1, periodic_check, (sc,))


if __name__ == "__main__":
    # Initial scheduling 
    scheduler.enter(0, 1, periodic_check, (scheduler,))
    scheduler.run()