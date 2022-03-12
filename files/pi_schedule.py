import threading
import time
import schedule
import os

# after edit run the command: sudo supervisorctl restart schedulers

def list_telebit():
    print("hello world")
    

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(30).minutes.do(run_threaded, list_telebit)


while True:
    schedule.run_pending()
    time.sleep(1)