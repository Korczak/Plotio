
class PlotterSettings:
    def __init__(self, speed_of_motors: int, hit_count: int, pixel_density: int) -> None:
        self.speed_of_motors: int = speed_of_motors
        self.hit_count: int = hit_count
        self.pixel_density: int = pixel_density
