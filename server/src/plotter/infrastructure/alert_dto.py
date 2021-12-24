import enum
from src.plotter.domain.alert import AlertType

class AlertDto:
    def __init__(self, text: str, type: AlertType) -> None:
        self.text: str = text
        self.type: AlertType = type