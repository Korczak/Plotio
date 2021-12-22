import enum
from typing import List, Optional


class Image:
    def __init__(self, name: str, content: str) -> None:
        self.name = name
        self.content = content