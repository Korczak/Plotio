from datetime import datetime
import enum
from typing import Any
from src.plotter.domain.alarm import AlarmType

class AlarmDto:
    def __init__(self, text: str, type: AlarmType, enabled: bool, ignore_end_time: datetime) -> None:
        self.text: str = text
        self.type: AlarmType = type
        self.enabled: bool = enabled
        self.ignore_end_time: datetime = ignore_end_time