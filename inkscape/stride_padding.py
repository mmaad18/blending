

def draw_number(x, y, size, number=0):
    text(str(number), (x + size/2.25, y + size/1.25), font_size='24pt', font_family='serif')


def draw_box(x, y, size, spacing=1, stroke_width=1, stroke='black'):
    rect((x + spacing, y + spacing), (x + size, y + size), fill='none', stroke=stroke, stroke_width=stroke_width)


def draw_kernel(x, y, size, multiplier=3, stroke_width=3, stroke='red'):
    rect((x, y), (x + multiplier*size, y + multiplier*size), fill='none', stroke=stroke, stroke_width=stroke_width, stroke_linecap='round')


def draw_right_arrow(x, y, base_length, base_height, head_length, head_height, color='black'):
    bl = base_length
    bh2 = base_height / 2
    hh2 = head_height / 2
    tl = base_length + head_length
    polygon([(x, y), (x, y + bh2), (x + bl, y + bh2), (x + bl, y + hh2),
             (x + tl, y), (x + bl, y - hh2), (x + bl, y - bh2), (x, y - bh2)],
            fill=color, stroke=color, stroke_width=2)


# Define some program parameters.
canvas.width = 550
canvas.height = 550
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
            draw_box(x, y, size, spacing=spacing, stroke_width=2, stroke='black')


draw_kernel(spacing/2, spacing/2, size, stroke_width=4, stroke='red')
draw_kernel(spacing/2 + size, spacing/2, size, stroke_width=3, stroke='blue')
draw_kernel(spacing/2 + 2*size, spacing/2, size, stroke_width=2, stroke='green')


draw_right_arrow(spacing/2, size/2 + spacing, size*0.7, size*0.15, size*0.25, size*0.35, color='blue')
draw_right_arrow(spacing/2, size*1.5 + spacing, size*1.7, size*0.15, size*0.25, size*0.35, color='green')
