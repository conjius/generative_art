from canvas import Canvas
from leaf import LeafDrawer

num_rows = 5
num_cols = 5
canvas_size = (1280, 1280)


def main():
    canvas = Canvas(*canvas_size, is_antialias=True)
    leaf_drawer = LeafDrawer(canvas)
    # leaf_drawer.draw_leaf()
    leaf_drawer.draw_leaves(num_rows=num_rows, num_cols=num_cols)


if __name__ == "__main__":
    main()
