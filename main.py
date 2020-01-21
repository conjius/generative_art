from PIL import Image, ImageDraw
import aggdraw


class Measurements:
    class Canvas:
        height = 512
        width = height
        size = (height, width)

    class Pen:
        thickness = 10


class Leaf:
    top_pt = (Measurements.Canvas.width // 2, Measurements.Canvas.height // 3)
    top_left_handle = (Measurements.Canvas.width // 4, Measurements.Canvas.height // 3)
    top_right_handle = (Measurements.Canvas.width * 3 // 4, Measurements.Canvas.height // 3)

    bottom_pt = (Measurements.Canvas.width // 2, Measurements.Canvas.height * 6 // 10)
    bottom_left_handle = (Measurements.Canvas.width // 4, Measurements.Canvas.height * 2 // 3)
    bottom_right_handle = (Measurements.Canvas.width * 3 // 4, Measurements.Canvas.height * 2 // 3)

    stem_bottom_pt = (Measurements.Canvas.width // 2, Measurements.Canvas.height * 2 // 3)


class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)


def main():
    image = Image.new('RGBA', Measurements.Canvas.size, Color.white)
    canvas = aggdraw.Draw(image)
    pen = aggdraw.Pen(color=Color.black, width=Measurements.Pen.thickness)
    path = aggdraw.Path()

    # left line
    path.moveto(*Leaf.top_pt)
    path.curveto(*Leaf.top_left_handle, *Leaf.bottom_left_handle, *Leaf.bottom_pt)
    canvas.path(path, path, pen)

    # right line
    path.moveto(*Leaf.top_pt)
    path.curveto(*Leaf.top_right_handle, *Leaf.bottom_right_handle, *Leaf.bottom_pt)
    canvas.path(path, path, pen)

    # center line
    path.moveto(*Leaf.top_pt)
    path.lineto(*Leaf.bottom_pt)
    canvas.path(path, path, pen)

    # stem
    path.moveto(*Leaf.bottom_pt)
    path.lineto(*Leaf.stem_bottom_pt)
    canvas.path(path, path, pen)

    canvas.setantialias(True)
    canvas.flush()
    # canvas.ellipse([Measurements.canvas_width // 2.5, Measurements.canvas_height // 2.5,
    #                 Measurements.canvas_width - Measurements.canvas_width / 2.5,
    #                 Measurements.canvas_height - Measurements.canvas_height / 2.5], outline=Color.black,
    #                width=Measurements.line_thickness)
    image.show()


if __name__ == "__main__":
    main()
