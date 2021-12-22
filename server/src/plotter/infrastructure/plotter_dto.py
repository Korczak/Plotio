import enum
from src.plotter.domain.plotter_position import PlotterPosition

class PlotterDto:
    def __init__(self, status: str, plotterMode: str, workMode: str, position: PlotterPosition) -> None:
        self.status = status
        self.plotterMode = plotterMode
        self.workMode = workMode
        self.posX: float = position.posX
        self.posY: float = position.posY
        self.isHit: 0 | 1 = position.isHit