
from datetime import datetime
import sched
import time
import sqlite3

# Function to check medicion schedule
def check_medicion_schedule():
    conn = sqlite3.connect('db.sqlite3')
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_prescrition')
            rows = cursor.fetchall()
            
            current_time = datetime.now().time()  # Get current time
            
            for row in rows:
                medicion_time = row[1]  # Assuming the second column contains the medicion time
                print("medicion_timemedicion_time",row)
                if current_time.hour == medicion_time.hour and current_time.minute == medicion_time.minute:
                    print("Time for medicion!")  # Perform your action here (e.g., send notification, execute task)
                    break
                
        except Exception as e:
            print("Error executing SQL query:", e)
        finally:
            cursor.close()
            conn.close()
    else:
        print("Database connection not established.")

# Scheduler instance
scheduler = sched.scheduler(time.time, time.sleep)

# Function to periodically check medicion schedule
def periodic_check(sc):
    check_medicion_schedule()
    # Reschedule the check every 1 minute (adjust as needed)
    scheduler.enter(60, 1, periodic_check, (sc,))

# Start the scheduler
if __name__ == "__main__":
    # Initial scheduling of the periodic check
    scheduler.enter(0, 1, periodic_check, (scheduler,))
    scheduler.run()