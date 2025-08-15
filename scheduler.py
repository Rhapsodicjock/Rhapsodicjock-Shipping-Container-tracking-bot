import schedule, time
from typing import Callable

def run_daily(at_time: str, job: Callable[[], None]):
    schedule.every().day.at(at_time).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
