from png import write
from png_animation import write_animation
from random import randrange


def examples():
    example_png()
    example_animation()


def example_png(path='example_01_frame.png'):
    def random_color():
        r = lambda: randrange(0xff)
        return (r(), r(), r())

    size = 200
    frame = []
    for _ in range(size):
        row = [random_color() for _ in range(size)]
        frame.append(row)
    write(frame, path)


def example_animation(path='example_02_animation.png'):
    size = 100

    def row():
        return [None] * size

    grid = [row() for _ in range(size)]
    q1 = lambda: randrange(0, size / 4)
    q4 = lambda: randrange(size - size / 4, size)
    frames = []
    for n in range(200):
        v = randrange(0xff)
        c = (v, v, v)
        x0, y0 = q1(), q1()
        x1, y1 = q4(), q4()
        xs = range(x0, x1)
        ys = range(y0, y1)
        for x, y in zip(xs, ys):  # Cool algorithm bro :/
            grid[y][x] = c
        copy = [row[:] for row in grid]
        frames.append(copy)
    print('animating...')
    write_animation(frames, path)
    print('done!')

if __name__ == '__main__':
    examples()