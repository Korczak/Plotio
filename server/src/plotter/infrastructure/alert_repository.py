from typing import List
from src.plotter.domain.alert import Alert, AlertType

from src.plotter.infrastructure.alert_dto import AlertDto



class AlertRepository:    
    def __init__(self) -> None:
        self._alert_db: List[AlertDto] = [AlertDto("System został uruchomiony poprawnie", AlertType.Success)]

    def add_alert(self, alert: Alert):
        self._alert_db.append(AlertDto(alert.text, alert.type))

    def get_alerts(self) -> List[Alert]:
        return [Alert(alert.text, alert.type) for alert in self._alert_db]
        
            
