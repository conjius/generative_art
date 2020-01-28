from typing import Tuple

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
        self._path = aggdraw.Path()
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

    def add_line(self, start_pt: Tuple[int, int], end_pt: Tuple[int, int]) -> None:
        """
        Adds a line to the canvas' current path, from point start_pt to point end_pt.
        :param start_pt: the line's start point.
        :param end_pt: the line's end point.
        """
        self._path.moveto(*start_pt)
        self._path.lineto(*end_pt)

    def add_curve(self, start_pt: Tuple[int, int], end_pt: Tuple[int, int], start_handle: Tuple[int, int],
                  end_handle: Tuple[int, int], ) -> None:
        """
        Adds a curve to the canvas' current path, from point start_pt to point end_pt,
        and the Bezier curve handles start_handle and end_handle.
        :param start_pt: the Bezier curve's start point.
        :param end_pt: the Bezier curve's end point.
        :param start_handle: the Bezier curve's start point's handle point.
        :param end_handle: the Bezier curve's end point's handle point.
        """
        self._path.moveto(*start_pt)
        self._path.curveto(*start_handle, *end_handle, *end_pt)

    def draw_last_line_or_curve(self, pen: Pen = None, brush: Brush = None) -> None:
        """
        Draws the canvas' current path onto the canvas using the provided Pen and Brush instances.
        If no Pen or Brush instances are provided, the canvas' default_pen Pen instance and default_brush instances
        are used.
        :param pen: the Pen instance to use to draw this curve. If no Pen instance is provided, the canvas' default_pen
        Pen instance is used.
        :param brush: the Brush instance to use to fill this curve. If no Brush instance is provided, the canvas'
        default_brush Brush instance is used.
        """
        brush = self.default_brush if brush is None else brush
        pen = self.default_pen if pen is None else pen

        # Draw the path
        self.agg_canvas.path(self._path, pen.agg_pen, brush.agg_brush)
        self.agg_canvas.flush()

        # reset the canvas' path to a new aggdraw.Path instance
        self._path = aggdraw.Path()

    def resize(self, to_height: int, to_width: int):
        self.image = self.image.resize((to_width, to_height))

    def show(self) -> None:
        self.image.show()
