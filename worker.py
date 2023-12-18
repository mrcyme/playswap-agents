import schedule
import time
import threading

def run_threaded(job_func, *args, **kwargs):
    job_thread = threading.Thread(target=job_func, args=args, kwargs=kwargs)
    job_thread.start()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def get_job_by_name(name):
    for job in schedule.jobs:
        if hasattr(job.job_func, 'job_name') and job.job_func.job_name == name:
            return job
    return None

def pause_job(name):
    job = get_job_by_name(name)
    if job:
        job.enabled = False

def resume_job(name):
    job = get_job_by_name(name)
    if job:
        job.enabled = True
        
def delete_job(name):
    job = get_job_by_name(name)
    if job:
        schedule.cancel_job(job)


scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()