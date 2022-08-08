from array import array
import board
import displayio
import framebufferio
import math
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

colors = 64
palette = displayio.Palette(colors)
for i in range(colors):
    palette[i] = rainbowio.colorwheel(i*(256/colors))

bitmap1 = displayio.Bitmap(display.width, display.height, colors)
group1 = displayio.Group()
group1.append(displayio.TileGrid(bitmap1, pixel_shader=palette))

bitmap2 = displayio.Bitmap(display.width, display.height, colors)
group2 = displayio.Group()
group2.append(displayio.TileGrid(bitmap2, pixel_shader=palette))

lut = array('B', [colors + int(colors * math.sin(math.radians(x))) for x in range(360)])
 
shift = 0
xdiv, ydiv = 50.0, 30.0
xdv, ydv = 14.0/13.0, 8.0/7.0
min, max = 15.0, 60.0

def plasma(bitmap, shift, xdiv, ydiv):
    for y in range(bitmap.height):
        ysin = lut[int(360 * y / ydiv) % 360]
        for x in range(bitmap.width):
            xsin = lut[int(360 * x / xdiv) % 360]
            color = int((xsin + ysin)/2 + shift) % colors
            bitmap[x + y * bitmap.width] = color

while True:
    plasma(bitmap1, shift, xdiv, ydiv)
    display.show(group1)

    shift = (shift + 1) % colors
    xdiv += xdv
    if xdiv < min or xdiv > max:
        xdv = -xdv
    ydiv += ydv
    if ydiv < min or ydiv > max:
        ydv = -ydv

    plasma(bitmap2, shift, xdiv, ydiv)
    display.show(group2)

    shift = (shift + 1) % colors
    xdiv += xdv
    if xdiv < min or xdiv > max:
        xdv = -xdv
    ydiv += ydv
    if ydiv < min or ydiv > max:
        ydv = -ydv

