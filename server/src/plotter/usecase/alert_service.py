from enum import Enum
from typing import List
from pubsub import pub
from pydantic.main import BaseModel
from src.plotter.domain.alert import Alert, AlertType
from src.plotter.infrastructure.alert_repository import AlertRepository


class AlertModelEnum(str, Enum):
    Error = 'Error'
    Warning = 'Warning'
    Success = 'Success'
    
class AlertModel(BaseModel):
    text: str
    type: AlertModelEnum
   
class AlertResponse(BaseModel):
    alerts: List[AlertModel]
    
class AlertService:
    def __init__(self, alert_repository: AlertRepository) -> None:
        self.alert_repository: AlertRepository = alert_repository

    async def get_alerts(self) -> AlertResponse:
        alerts = self.alert_repository.get_alerts() 
        alerts_to_return = [AlertModel(text=alert.text, type=convert_to_enum(alert.type)) for alert in alerts]
        alerts_to_return.reverse()
        return AlertResponse(alerts=alerts_to_return)
    
    def subscribe(self):
        pub.subscribe(self.project_completed, 'ProjectCompleted')
        pub.subscribe(self.project_paused, 'ProjectPaused')
        pub.subscribe(self.project_stopped, 'ProjectStopped')
        pub.subscribe(self.project_started, 'ProjectStarted')
        pub.subscribe(self.project_resumed, 'ProjectResumed')

    def project_completed(self):
        self.alert_repository.add_alert(Alert("Ukończono projekt", AlertType.Success))
    def project_paused(self):
        self.alert_repository.add_alert(Alert("Spauzowano projekt", AlertType.Warning))
    def project_stopped(self):
        self.alert_repository.add_alert(Alert("Zastopowano projekt", AlertType.Warning))
    def project_started(self):
        self.alert_repository.add_alert(Alert("Rozpoczęto projekt", AlertType.Success))
    def project_resumed(self):
        self.alert_repository.add_alert(Alert("Wznowiono projekt", AlertType.Success))
        
        
def convert_to_enum(type: AlertType) -> AlertModelEnum:
    switch={
        AlertType.Success: AlertModelEnum.Success,
        AlertType.Error: AlertModelEnum.Error,
        AlertType.Warning: AlertModelEnum.Warning
    }
    
    return switch.get(type)
            