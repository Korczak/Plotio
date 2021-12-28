from typing import List, Optional
from src.plotter.domain.command import Command

class CommandGroup:
    def __init__(self, commands: List[Command]) -> None:
        self.commands: List[Command] = commands
    
    