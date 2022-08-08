import board
import displayio
import framebufferio
import rainbowio
import random
import rgbmatrix
import time

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=5,
    rgb_pins=[board.MTX_R1, board.MTX_G1, board.MTX_B1, board.MTX_R2, board.MTX_G2, board.MTX_B2],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

palette = displayio.Palette(32)
palette[0] = 0x000000
palette[1] = 0xFFFFFF

for i in range(16, 32):
    palette[i] = rainbowio.colorwheel((i-16)*16)

bitmap1 = displayio.Bitmap(display.width, display.height, 16)
group1 = displayio.Group()
group1.append(displayio.TileGrid(bitmap1, pixel_shader=palette))

bitmap2 = displayio.Bitmap(display.width, display.height, 16)
group2 = displayio.Group()
group2.append(displayio.TileGrid(bitmap2, pixel_shader=palette))

display.show(group1)

def init_random(bitmap, fraction=0.3):
    for i in range(bitmap.height * bitmap.width):
        bitmap[i] = random.random() < fraction
    return 500

def init_tribute(bitmap):
    # Based on xkcd's tribute to John Conway (1937-2020) https://xkcd.com/2293/

    x = bitmap.width // 2 - 3
    y = bitmap.height // 2 - 5

    bitmap.fill(0)

    bitmap[(x+2) + (y+0)*bitmap.width] = 1
    bitmap[(x+3) + (y+0)*bitmap.width] = 1
    bitmap[(x+4) + (y+0)*bitmap.width] = 1

    bitmap[(x+2) + (y+1)*bitmap.width] = 1
    bitmap[(x+4) + (y+1)*bitmap.width] = 1

    bitmap[(x+2) + (y+2)*bitmap.width] = 1
    bitmap[(x+4) + (y+2)*bitmap.width] = 1

    bitmap[(x+3) + (y+3)*bitmap.width] = 1

    bitmap[(x+0) + (y+4)*bitmap.width] = 1
    bitmap[(x+2) + (y+4)*bitmap.width] = 1
    bitmap[(x+3) + (y+4)*bitmap.width] = 1
    bitmap[(x+4) + (y+4)*bitmap.width] = 1

    bitmap[(x+1) + (y+5)*bitmap.width] = 1
    bitmap[(x+3) + (y+5)*bitmap.width] = 1
    bitmap[(x+5) + (y+5)*bitmap.width] = 1

    bitmap[(x+3) + (y+6)*bitmap.width] = 1
    bitmap[(x+6) + (y+6)*bitmap.width] = 1

    bitmap[(x+2) + (y+7)*bitmap.width] = 1
    bitmap[(x+4) + (y+7)*bitmap.width] = 1

    bitmap[(x+2) + (y+8)*bitmap.width] = 1
    bitmap[(x+4) + (y+8)*bitmap.width] = 1

    time.sleep(1)

    return 50

def apply_life_rule(old, new):
    width = old.width
    height = old.height
    for y in range(height):
        yyy = y * width
        ym1 = ((y + height - 1) % height) * width
        yp1 = ((y + 1) % height) * width
        xm1 = width - 1
        for x in range(width):
            xp1 = (x + 1) % width
            neighbors = (
                old[xm1 + ym1] + old[xm1 + yyy] + old[xm1 + yp1] +
                old[x   + ym1] +                  old[x   + yp1] +
                old[xp1 + ym1] + old[xp1 + yyy] + old[xp1 + yp1])
            new[x+yyy] = neighbors == 3 or (neighbors == 2 and old[x+yyy])
            xm1 = x

iters = init_tribute(bitmap1)

while True:
    for i in range(iters):
        display.show(group1)
        apply_life_rule(bitmap1, bitmap2)
        display.show(group2)
        apply_life_rule(bitmap2, bitmap1)

    palette[1] = palette[random.randint(16, 31)]
    if random.random() < 0.05:
        iters = init_tribute(bitmap1)
    else:
        iters = init_random(bitmap1)
