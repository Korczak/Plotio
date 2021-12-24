
class PlotterSettingsDto:
    def __init__(self, speed_of_motors: int, speed_of_Z: int) -> None:
        self.speed_of_motors: int = speed_of_motors
        self.speed_of_Z: int = speed_of_Z
