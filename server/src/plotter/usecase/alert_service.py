from enum import Enum
from typing import List
from pydantic.main import BaseModel
from src.plotter.domain.alert import AlertType
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
    
def convert_to_enum(type: AlertType) -> AlertModelEnum:
    switch={
        AlertType.Success: AlertModelEnum.Success,
        AlertType.Error: AlertModelEnum.Error,
        AlertType.Warning: AlertModelEnum.Warning
    }
    
    return switch.get(type)
            