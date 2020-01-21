from typing import Tuple

from canvas import Canvas
import random


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
        self.canvas = canvas

    def create_random_leaf(self) -> Leaf:
        # points
        top_pt = (self.canvas.width // 2, self.canvas.height // 5)
        bottom_pt = (self.canvas.width // 2, self.canvas.height * 6 // 10)
        stem_bottom_pt = (self.canvas.width // 2, self.canvas.height * 4 // 5)

        # Bezier curve handle points
        top_left_handle = (random.randint(0, self.canvas.width * 4 // 10),
                           random.randint(0, self.canvas.height // 2))
        bottom_left_handle = (random.randint(0, self.canvas.width * 4 // 10),
                              random.randint(self.canvas.height // 2, self.canvas.height))
        top_right_handle = (self.canvas.width - top_left_handle[0], top_left_handle[1])
        bottom_right_handle = (self.canvas.width - bottom_left_handle[0], bottom_left_handle[1])

        # create and return the actual Leaf instance
        return Leaf(top_pt=top_pt, bottom_pt=bottom_pt, stem_bottom_pt=stem_bottom_pt,
                    top_left_handle=top_left_handle, bottom_left_handle=bottom_left_handle,
                    top_right_handle=top_right_handle, bottom_right_handle=bottom_right_handle)


class LeafDrawer:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.leaf_factory = LeafFactory(self.canvas)

    def draw_leaf(self) -> None:
        leaf = self.leaf_factory.create_random_leaf()

        # left curve
        self.canvas.draw_curve(start_pt=leaf.top_pt, end_pt=leaf.bottom_pt,
                               start_handle=leaf.top_left_handle, end_handle=leaf.bottom_left_handle)

        # right curve
        self.canvas.draw_curve(start_pt=leaf.top_pt, end_pt=leaf.bottom_pt,
                               start_handle=leaf.top_right_handle, end_handle=leaf.bottom_right_handle)

        # center line
        self.canvas.draw_line(leaf.top_pt, leaf.bottom_pt)

        # stem line
        self.canvas.draw_line(leaf.bottom_pt, leaf.stem_bottom_pt)

        self.canvas.render()

    def draw_leaves(self, num_rows: int, num_cols: int) -> None:
        raise NotImplementedError
