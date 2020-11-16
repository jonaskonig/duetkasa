from datetime import datetime
from datetime import timedelta

class Timer:
    def __init__(minutes):
        self.minutes = datetime.now() + timedelta(minutes=minutes)

    def timer_up(self):
        return (self.minutes <= datetime.now())
