from enum import Enum
from typing import List
from pubsub import pub
from pydantic.main import BaseModel
from src.plotter.domain.alarm import Alarm
from src.plotter.domain.alert import AlertType
from src.plotter.domain.plotter import Plotter
from src.plotter.infrastructure.alarm_repository import AlarmRepository
from src.plotter.infrastructure.alert_repository import AlertRepository
from src.plotter.infrastructure.plotter_repository import PlotterRepository


class AlarmResponse(BaseModel):
    is_alarm: bool
    message: str
    
class AlarmService:
    def __init__(self, alarm_repository: AlarmRepository, plotter_repository: PlotterRepository) -> None:
        self.alarm_repository: AlarmRepository = alarm_repository
        self.plotter_repository: PlotterRepository = plotter_repository

    async def get_alarm(self) -> AlarmResponse:
        alarm = self.alarm_repository.get_alarm() 
        if(alarm == None or alarm.enabled == False or alarm.is_ignored() == True):
            return AlarmResponse(is_alarm=False, message="")
        
        return AlarmResponse(is_alarm=True, message=alarm.text)
    
    async def reset_alarm(self):
        plotter: Plotter = self.plotter_repository.get_plotter()
        if(plotter.alarm != None):
            plotter.reset_alarm()
            self.plotter_repository.update_plotter(plotter)
            
    async def ignore_alarm(self):
        plotter: Plotter = self.plotter_repository.get_plotter()
        if(plotter.alarm != None):
            plotter.ignore_alarm()
            self.plotter_repository.update_plotter(plotter)
               
    def subscribe(self):
        pub.subscribe(self.on_alarm_set, 'PlotterAlarmSet')

    def on_alarm_set(self, arg1: Alarm):
        plotter: Plotter = self.plotter_repository.get_plotter()
        if(plotter.is_alarm_active() == False):
            plotter.set_alarm(arg1)
            self.plotter_repository.update_plotter(plotter)