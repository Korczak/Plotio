import enum
from typing import Any, List, Optional
import datetime

class AlarmType(enum.Enum):
    Error = 'Error'
class Alarm:
    def __init__(self, text: str, type: AlarmType, enabled: bool, ignore_end_time: datetime) -> None:
        self.text: str = text
        self.type: AlarmType = type
        self.enabled: bool = enabled
        self.ignore_end_time: datetime = ignore_end_time
        
    def disable_alarm(self):
        self.enabled = False
        
    def ignore_alarm(self, timeout: int):
        self.ignore_end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        
    def is_ignored(self):
        if(self.ignore_end_time == None):
            return False
        if(datetime.datetime.now() > self.ignore_end_time):
            #self.ignore_end_time = None
            return False
        return True