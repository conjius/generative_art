from os import path, mkdir
from typing import Tuple, List
from uuid import uuid4
import random

from canvas import Canvas
from colors import Color
from utensils import Brush, Pen


class Leaf:
    def __init__(self, left_pts: List[Tuple[int, int]], right_pts: List[Tuple[int, int]],
                 stem_bottom_pt: Tuple[int, int],
                 left_handle_pairs: List[Tuple[Tuple[object, object], Tuple[object, object]]],
                 right_handle_pairs: List[Tuple[Tuple[object, object], Tuple[object, object]]]):
        # points
        self.left_pts, self.right_pts = left_pts, right_pts
        self.stem_bottom_pt = stem_bottom_pt

        # Bezier curve handle points
        self.left_handle_pairs, self.right_handle_pairs = left_handle_pairs, right_handle_pairs


class LeafFactory:
    def __init__(self, canvas: Canvas):
        self._canvas = canvas

    def create_random_leaf(self, max_num_teeth: int = 5) -> Leaf:
        # the number of "teeth" to apply to the edge of the leaf
        num_teeth = random.randint(1, max_num_teeth)
        # num_teeth = 2

        # points
        top_pt = (self._canvas.width // 2, self._canvas.height // 5)
        bottom_pt = (self._canvas.width // 2, self._canvas.height * 6 // 10)
        stem_bottom_pt = (self._canvas.width // 2, self._canvas.height * 4 // 5)
        vertical_interval_between_pts = (bottom_pt[1] - top_pt[1]) // num_teeth

        left_pts = [top_pt] + \
                   [(random.randint(self._canvas.width // 5, self._canvas.width // 2),
                     top_pt[1] + (i + 1) * vertical_interval_between_pts) for i in range(num_teeth - 1)] + \
                   [bottom_pt]

        right_pts = [top_pt] + [(self._canvas.width - x, y) for x, y in left_pts[1:-1]] + [bottom_pt]

        # Bezier curve handle points
        top_left_handle = (random.randint(0, self._canvas.width * 4 // 10),
                           random.randint(0, self._canvas.height // 2))
        bottom_left_handle = (random.randint(0, self._canvas.width * 4 // 10),
                              random.randint(self._canvas.height // 2, self._canvas.height))
        top_right_handle = (self._canvas.width - top_left_handle[0], top_left_handle[1])
        bottom_right_handle = (self._canvas.width - bottom_left_handle[0], bottom_left_handle[1])
        left_handle_pairs = [((None, None), top_left_handle)] + \
                            [((random.randint(0, self._canvas.width * 4 // 10),
                               top_left_handle[1] + i * vertical_interval_between_pts),
                              (random.randint(0, self._canvas.width * 4 // 10),
                               top_left_handle[1] + (i + 1) * vertical_interval_between_pts))
                             for i in range(num_teeth + 1)] + [(bottom_left_handle, (None, None))]
        right_handle_pairs = [((None, None), top_right_handle)] + \
                             [((self._canvas.width - pair[0][0], pair[0][1]),
                               (self._canvas.width - pair[1][0], pair[1][1])) for pair in left_handle_pairs[1:-1]] + \
                             [(bottom_right_handle, (None, None))]

        # create and return the actual Leaf instance
        return Leaf(left_pts=left_pts, right_pts=right_pts, stem_bottom_pt=stem_bottom_pt,
                    left_handle_pairs=left_handle_pairs, right_handle_pairs=right_handle_pairs)


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
        pen = Pen(thickness=20, color=Color.get_random_outline_color())

        leaf = self._leaf_factory.create_random_leaf()

        # left leaf edge
        for i in range(len(leaf.left_pts) - 1):
            self._canvas.add_curve(start_pt=leaf.left_pts[i], end_pt=leaf.left_pts[i + 1],
                                   start_handle=leaf.left_handle_pairs[i][1],
                                   end_handle=leaf.left_handle_pairs[i + 1][0],
                                   pen=pen, brush=brush)

        # right leaf edge
        for i in range(len(leaf.right_pts) - 1):
            self._canvas.add_curve(start_pt=leaf.right_pts[i], end_pt=leaf.right_pts[i + 1],
                                   start_handle=leaf.right_handle_pairs[i][1],
                                   end_handle=leaf.right_handle_pairs[i + 1][0],
                                   pen=pen, brush=brush)

        # center line
        self._canvas.add_line(leaf.left_pts[0],
                              leaf.left_pts[-1],
                              pen=pen)  # the fact that left and not right was selected here is arbitrary

        # stem line
        self._canvas.add_line(leaf.left_pts[-1], leaf.stem_bottom_pt, pen=pen)  # the same goes for here

        self._canvas.show()

    def draw_leaves(self, num_rows: int, num_cols: int, save_to_file=False) -> None:
        if num_cols != num_rows:
            raise ValueError("num_rows and num_cols must be equal for a nice-looking grid.")

        self._is_grid = True
        self._main_canvas = Canvas.from_canvas(self._canvas)
        self._sub_canvases = [[Canvas.from_canvas(self._canvas, is_randomize_bg=True) for row in range(num_rows)] for
                              col in range(num_cols)]
        for row in range(num_rows):
            for col in range(num_cols):
                leaf = self._leaf_factory.create_random_leaf()
                brush = Brush(color=Color.get_random_leaf_color())
                pen = Pen(thickness=25, color=Color.get_random_outline_color())

                # left leaf edge
                for i in range(len(leaf.left_pts) - 1):
                    self._sub_canvases[row][col].add_curve(start_pt=leaf.left_pts[i], end_pt=leaf.left_pts[i + 1],
                                                           start_handle=leaf.left_handle_pairs[i][1],
                                                           end_handle=leaf.left_handle_pairs[i + 1][0])

                # "left" center line - used to close the left-hand-side Path of the leaf
                self._sub_canvases[row][col].add_line(leaf.left_pts[0], leaf.left_pts[-1])
                self._sub_canvases[row][col].draw_last_line_or_curve(pen=pen, brush=brush)

                # right leaf edge
                for i in range(len(leaf.right_pts) - 1):
                    self._sub_canvases[row][col].add_curve(start_pt=leaf.right_pts[i], end_pt=leaf.right_pts[i + 1],
                                                           start_handle=leaf.right_handle_pairs[i][1],
                                                           end_handle=leaf.right_handle_pairs[i + 1][0])

                # "right" center line - used to close the right-hand-side Path of the leaf
                self._sub_canvases[row][col].add_line(leaf.right_pts[0], leaf.right_pts[-1])
                self._sub_canvases[row][col].draw_last_line_or_curve(pen=pen, brush=brush)

                # stem line
                self._sub_canvases[row][col].add_line(leaf.left_pts[-1], leaf.stem_bottom_pt)
                self._sub_canvases[row][col].draw_last_line_or_curve(pen=pen, brush=brush)

                # resize each canvas to fit in grid
                self._resized_sub_canvases_size = (self._main_canvas.width // num_cols,
                                                   self._main_canvas.height // num_rows)
                self._sub_canvases[row][col].resize(to_height=self._resized_sub_canvases_size[1],
                                                    to_width=self._resized_sub_canvases_size[0])
                self._main_canvas.image.paste(self._sub_canvases[row][col].image, self._grid_offsets)
                self._grid_offsets = (self._grid_offsets[0] + self._resized_sub_canvases_size[0], self._grid_offsets[1])
            self._grid_offsets = (0, self._grid_offsets[1] + self._resized_sub_canvases_size[1])
        if save_to_file:
            if not path.exists("./images"):
                mkdir("./images")
            self._main_canvas.image.save(fp=f"./images/{uuid4()}.png", format="PNG")
        self._main_canvas.show()
