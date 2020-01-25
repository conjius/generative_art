from typing import Tuple
from copy import deepcopy

from PIL import Image
import aggdraw

from colors import Color
from utensils import Pen, Brush


class Canvas:
    def __init__(self, height: int, width: int, bg_color: Color = Color.get_random_color(),
                 default_pen: Pen = Pen(), default_brush: Brush = Brush(),
                 is_antialias: bool = False):
        """
        Constructs a new Canvas with the given background Color and size.
        :param height: the height of the canvas in pixels.
        :param width: the width of the canvas in pixels.
        :param bg_color: the background Color of the canvas.
        """
        self.height = height
        self.width = width
        self.bg_color = bg_color
        self.default_pen = default_pen
        self.default_brush = default_brush
        self.is_antialias = is_antialias

        # the base image under the canvas
        self.image = Image.new('RGB', (height, width), self.bg_color)

        # the actual canvas (on top of the base image) to draw on
        self.agg_canvas = aggdraw.Draw(self.image)
        self.agg_canvas.setantialias(self.is_antialias)

    @staticmethod
    def from_canvas(original: 'Canvas', is_randomize_bg: bool = False):
        return Canvas(height=original.height, width=original.width,
                      bg_color=Color.get_random_color() if is_randomize_bg else original.bg_color,
                      default_pen=original.default_pen, is_antialias=original.is_antialias)

    def draw_line(self, start_pt: Tuple[int, int], end_pt: Tuple[int, int], pen: Pen = None) -> None:
        """
        Draws a line on the canvas from point start_pt to point end_pt using the provided Pen instance.
        :param start_pt: the line's start point.
        :param end_pt: the line's end point.
        :param pen: the Pen instance to use to draw this line. If no Pen instance is provided, the canvas' default_pen
        Pen instance is used.
        """
        pen = self.default_pen if pen is None else pen
        path = aggdraw.Path()
        path.moveto(*start_pt)
        path.lineto(*end_pt)
        self.agg_canvas.path(path, path, pen.agg_pen)
        self.agg_canvas.flush()

    def draw_curve(self, start_pt: Tuple[int, int], end_pt: Tuple[int, int], start_handle: Tuple[int, int],
                   end_handle: Tuple[int, int], pen: Pen = None, brush: Brush = None) -> None:
        """
        Draws a line on the canvas from point start_pt to point end_pt using the provided Pen instance.
        :param start_pt: the line's start point.
        :param end_pt: the line's end point.
        :param start_handle: the Bezier curve's start point's handle point.
        :param end_handle: the Bezier curve's end point's handle point.
        :param pen: the Pen instance to use to draw this curve. If no Pen instance is provided, the canvas' default_pen
        Pen instance is used.
        :param brush: the Brush instance to use to fill this curve. If no Brush instance is provided, the canvas'
        default_brush Brush instance is used.
        """
        pen = self.default_pen if pen is None else pen
        brush = self.default_brush if brush is None else brush
        path = aggdraw.Path()
        path.moveto(*start_pt)
        path.curveto(*start_handle, *end_handle, *end_pt)
        self.agg_canvas.path(path, pen.agg_pen, brush.agg_brush)
        self.agg_canvas.flush()

    def resize(self, to_height: int, to_width: int):
        self.image = self.image.resize((to_width, to_height))

    def render(self) -> None:
        self.image.show()
