


def draw_number(x, y, size, number=0):
    text(str(number), (x + size/2.25, y + size/1.25), font_size='24pt', font_family='serif')


def draw_box(x, y, size, spacing=1, stroke_width=1, stroke='black'):
    rect((x + spacing, y + spacing), (x + size, y + size), fill='none', stroke=stroke, stroke_width=stroke_width)


def draw_kernel(x, y, size, multiplier=3, stroke_width=3, stroke='red'):
    rect((x, y), (x + multiplier*size, y + multiplier*size), fill='none', stroke=stroke, stroke_width=stroke_width, stroke_linecap='round')


# Define some program parameters.
canvas.width = 500
canvas.height = 500
x = 0
y = 0
size = 50
#stride = 100
spacing = 5
num_squares = 10
max_num = 9
min_num = 0
padding = 2


for i in range(num_squares):
    for j in range(num_squares):
        x = i * size
        y = j * size

        if i < padding or i >= num_squares - padding or j < padding or j >= num_squares - padding:
            draw_number(x, y, size)
            draw_box(x, y, size, spacing=spacing, stroke_width=1, stroke='#bbbbbb')
        else:
            draw_number(x, y, size, randint(min_num, max_num))
            #rect((x + spacing, y + spacing), (x + size, y + size), fill='none', stroke='black', stroke_width=1)
            draw_box(x, y, size, spacing=spacing, stroke_width=2, stroke='black')


draw_kernel(spacing/2, spacing/2, size)

draw_kernel(spacing/2 + size, spacing/2, size, multiplier=3, stroke_width=2, stroke='blue')

