import enum
from typing import List, Optional

class AlertType(enum.Enum):
    Error = 'Error'
    Warning = 'Warning'
    Success = 'Success'
    
class Alert:
    def __init__(self, text: str, type: AlertType) -> None:
        self.text: str = text
        self.type: AlertType = type
        