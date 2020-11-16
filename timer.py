from datetime import datetime
from datetime import timedelta

class Timer:
    def __init__(minutes):
        self.timetimer = datetime.now() + timedelta(minutes=minutes)

    def timer_up(self):
        return (self.timetimer <= datetime.now())
