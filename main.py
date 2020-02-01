from canvas import Canvas
from leaf import LeafDrawer

num_rows = 4
num_cols = 4
canvas_size = (1280, 1280)


def main():
    canvas = Canvas(*canvas_size, is_antialias=True)
    leaf_drawer = LeafDrawer(canvas, is_svg=True)

    # generate a single leaf
    # leaf_drawer.draw_single_leaf()

    # generate a grid of leaves
    leaf_drawer.draw_multiple_leaves(num_rows=num_rows, num_cols=num_cols, save_to_file=True)


if __name__ == "__main__":
    main()
