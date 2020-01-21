import aggdraw
from colors import Color


class Pen:
    def __init__(self, thickness: int, color=Color.black):
        self.color = color
        self.thickness = thickness
        self.agg_pen = aggdraw.Pen(color=self.color, width=self.thickness)
