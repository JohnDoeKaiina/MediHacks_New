import sched
import time

# Create a scheduler instance
scheduler = sched.scheduler(time.time, time.sleep)

# Example function to be executed
def print_hi():
    print("hi")

# Example function with an argument
def print_message(message):
    print(message)

# Schedule printing "hi" every hour
def schedule_hi():
    scheduler.enter(0, 1, print_hi, ())  # Schedule immediately
    scheduler.enter(3600, 1, schedule_hi, ())  # Schedule next execution after 1 hour (3600 seconds)

# Schedule printing a message with an argument
def schedule_message():
    message = "Hello from scheduler!"
    scheduler.enter(0, 1, print_message, (message,))  # Schedule immediately

# Start the scheduler in a separate thread
def start_scheduler():
    scheduler.run()

# Run the scheduler
if __name__ == "__main__":
    schedule_hi() 
    schedule_message()  # Start scheduling the message

    start_scheduler()  # Start the scheduler in a separate thread or process
