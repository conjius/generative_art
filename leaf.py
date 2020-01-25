from typing import Tuple
import random

from canvas import Canvas
from colors import Color
from utensils import Brush, Pen


class Leaf:
    def __init__(self, top_pt: Tuple[int, int], bottom_pt: Tuple[int, int], stem_bottom_pt: Tuple[int, int],
                 top_left_handle: Tuple[int, int], bottom_left_handle: Tuple[int, int],
                 top_right_handle: Tuple[int, int], bottom_right_handle: Tuple[int, int]):
        # points
        self.top_pt, self.bottom_pt, self.stem_bottom_pt = top_pt, bottom_pt, stem_bottom_pt

        # Bezier curve handle points
        self.top_left_handle, self.bottom_left_handle = top_left_handle, bottom_left_handle
        self.top_right_handle, self.bottom_right_handle = top_right_handle, bottom_right_handle


class LeafFactory:
    def __init__(self, canvas: Canvas):
        self._canvas = canvas

    def create_random_leaf(self) -> Leaf:
        # points
        top_pt = (self._canvas.width // 2, self._canvas.height // 5)
        bottom_pt = (self._canvas.width // 2, self._canvas.height * 6 // 10)
        stem_bottom_pt = (self._canvas.width // 2, self._canvas.height * 4 // 5)

        # Bezier curve handle points
        top_left_handle = (random.randint(0, self._canvas.width * 4 // 10),
                           random.randint(0, self._canvas.height // 2))
        bottom_left_handle = (random.randint(0, self._canvas.width * 4 // 10),
                              random.randint(self._canvas.height // 2, self._canvas.height))
        top_right_handle = (self._canvas.width - top_left_handle[0], top_left_handle[1])
        bottom_right_handle = (self._canvas.width - bottom_left_handle[0], bottom_left_handle[1])

        # create and return the actual Leaf instance
        return Leaf(top_pt=top_pt, bottom_pt=bottom_pt, stem_bottom_pt=stem_bottom_pt,
                    top_left_handle=top_left_handle, bottom_left_handle=bottom_left_handle,
                    top_right_handle=top_right_handle, bottom_right_handle=bottom_right_handle)


class LeafDrawer:
    def __init__(self, canvas: Canvas):
        self._canvas = canvas
        self._sub_canvases = None
        self._main_canvas = None
        self._leaf_factory = LeafFactory(self._canvas)
        self._is_grid = False
        self._grid_offsets: Tuple[int, int] = (0, 0)
        self._resized_sub_canvases_size = None

    def draw_leaf(self) -> None:
        self._is_grid = False
        brush = Brush(color=Color.get_random_leaf_color())
        pen = Pen(thickness=30, color=Color.get_random_leaf_color())

        leaf = self._leaf_factory.create_random_leaf()

        # left curve
        self._canvas.draw_curve(start_pt=leaf.top_pt, end_pt=leaf.bottom_pt,
                                start_handle=leaf.top_left_handle, end_handle=leaf.bottom_left_handle,
                                pen=pen, brush=brush)

        # right curve
        self._canvas.draw_curve(start_pt=leaf.top_pt, end_pt=leaf.bottom_pt,
                                start_handle=leaf.top_right_handle, end_handle=leaf.bottom_right_handle,
                                pen=pen, brush=brush)

        # center line
        self._canvas.draw_line(leaf.top_pt, leaf.bottom_pt)

        # stem line
        self._canvas.draw_line(leaf.bottom_pt, leaf.stem_bottom_pt)

        self._canvas.render()

    def draw_leaves(self, num_rows: int, num_cols: int) -> None:
        if num_cols != num_rows:
            raise ValueError("num_rows and num_cols must be equal for a nice-looking grid.")

        self._is_grid = True
        self._main_canvas = Canvas.from_canvas(self._canvas)
        self._sub_canvases = [[Canvas.from_canvas(self._canvas, is_randomize_bg=True) for row in range(num_rows)] for col in range(num_cols)]
        for row in range(num_rows):
            for col in range(num_cols):
                leaf = self._leaf_factory.create_random_leaf()
                brush = Brush(color=Color.get_random_leaf_color())
                pen = Pen(thickness=25, color=Color.get_random_leaf_color())

                # left curve
                self._sub_canvases[row][col].draw_curve(start_pt=leaf.top_pt, end_pt=leaf.bottom_pt,
                                                        start_handle=leaf.top_left_handle,
                                                        end_handle=leaf.bottom_left_handle,
                                                        pen=pen, brush=brush)

                # right curve
                self._sub_canvases[row][col].draw_curve(start_pt=leaf.top_pt, end_pt=leaf.bottom_pt,
                                                        start_handle=leaf.top_right_handle,
                                                        end_handle=leaf.bottom_right_handle,
                                                        pen=pen, brush=brush)

                # center line
                self._sub_canvases[row][col].draw_line(leaf.top_pt, leaf.bottom_pt)

                # stem line
                self._sub_canvases[row][col].draw_line(leaf.bottom_pt, leaf.stem_bottom_pt)

                # resize each canvas to fit in grid
                self._resized_sub_canvases_size = (self._main_canvas.width // num_cols,
                                                   self._main_canvas.height // num_rows)
                self._sub_canvases[row][col].resize(to_height=self._resized_sub_canvases_size[1],
                                                    to_width=self._resized_sub_canvases_size[0])
                self._main_canvas.image.paste(self._sub_canvases[row][col].image, self._grid_offsets)
                self._grid_offsets = (self._grid_offsets[0] + self._resized_sub_canvases_size[0], self._grid_offsets[1])
            self._grid_offsets = (0, self._grid_offsets[1] + self._resized_sub_canvases_size[1])
        self._main_canvas.render()
