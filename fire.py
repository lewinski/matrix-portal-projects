import board
import displayio
import framebufferio
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

palette = displayio.Palette(16)
palette[0] = 0x000000
palette[1] = 0x100000
palette[2] = 0x300000
palette[3] = 0x600000
palette[4] = 0x800000
palette[5] = 0xA00000
palette[6] = 0xC02000
palette[7] = 0xC04000
palette[8] = 0xC06000
palette[9] = 0xC08000
palette[10] = 0xC08030
ncolors = 11

bitmap1 = displayio.Bitmap(display.width, display.height, 16)
group1 = displayio.Group()
group1.append(displayio.TileGrid(bitmap1, pixel_shader=palette))

bitmap2 = displayio.Bitmap(display.width, display.height, 16)
group2 = displayio.Group()
group2.append(displayio.TileGrid(bitmap2, pixel_shader=palette))

display.show(group1)

def init_fire(bitmap, ncolors):
    bitmap.fill(0)
    for i in range(bitmap.width):
        bitmap[i, bitmap.height-1] = random.randint(0, ncolors)

def apply_fire_rule(old, new, ncolors):
    width = old.width
    height = old.height    
    for y in range(0, height - 1):
        for x in range(0, width):
            if random.random() < 0.45:
                new[x, y] = max(0, old[x, y+1] - 1)
            else:
                new[x, y] = max(0, old[x, y+1])
    for x in range(0, width):
        new[x, height-1] = random.randint(ncolors - 6, ncolors - 2)

init_fire(bitmap1, ncolors)
while True:
    display.show(group1)
    apply_fire_rule(bitmap1, bitmap2, ncolors)
    display.show(group2)
    apply_fire_rule(bitmap2, bitmap1, ncolors)

    time.sleep(0.03)
