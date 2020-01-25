import aggdraw
from colors import Color


class Pen:
    def __init__(self, thickness: int = 15, color: Color = Color.black):
        self.color = color
        self.thickness = thickness
        self.agg_pen = aggdraw.Pen(color=color, width=self.thickness)


class Brush:
    def __init__(self, color: Color = Color.get_random_color()):
        self.color = color
        self.agg_brush = aggdraw.Brush(color=color)
