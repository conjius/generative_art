from canvas import Canvas
from leaf import LeafDrawer

num_rows = 3
num_cols = 3
canvas_size = (768, 768)


def main():
    canvas = Canvas(*canvas_size)
    leaf_drawer = LeafDrawer(canvas)
    leaf_drawer.draw_leaf()
    # leaf_drawer.draw_leaves(num_rows=num_rows, num_cols=num_cols)


if __name__ == "__main__":
    main()
