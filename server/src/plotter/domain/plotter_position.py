

class PlotterPosition:
    def __init__(self, posX: float, posY: float, isHit: 0 | 1) -> None:
        self.posX: float = posX
        self.posY: float = posY
        self.isHit: 0 | 1 = isHit