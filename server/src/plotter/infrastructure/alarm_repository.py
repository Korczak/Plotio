from typing import List
from src.plotter.domain.alarm import Alarm
from src.plotter.infrastructure.alarm_dto import AlarmDto

class AlarmRepository:    
    def __init__(self) -> None:
        self._alarm_db: AlarmDto = None

    def add_alarm(self, alarm: Alarm):
        self._alarm_db = AlarmDto(alarm.text, alarm.type, alarm.enabled, alarm.ignore_end_time)

    def update_alarm(self, alarm: Alarm):
        if(alarm != None):
            self._alarm_db = AlarmDto(alarm.text, alarm.type, alarm.enabled, alarm.ignore_end_time)

    def get_alarm(self) -> Alarm:
        if self._alarm_db == None:
            return None
        return Alarm(self._alarm_db.text, self._alarm_db.type, self._alarm_db.enabled, self._alarm_db.ignore_end_time)
