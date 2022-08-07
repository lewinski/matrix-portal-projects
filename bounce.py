import board
import displayio
import framebufferio
import rainbowio
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

bitmap = displayio.Bitmap(display.width, display.height, 64)
group = displayio.Group()
group.append(displayio.TileGrid(bitmap, pixel_shader=palette))

display.show(group)

x, y = 5, 0
dx, dy = 1, 1
color = 16

while True:
    bitmap[x + y * display.width] = 0
    bounced = False

    x += dx
    y += dy
    if x == 0 or x == display.width - 1:
        dx = -dx
        bounced = True
    if y == 0 or y == display.height - 1:
        dy = -dy
        bounced = True

    if bounced:
        if color == 31:
            color = 16
        else:
            color += 1
    bitmap[x + y * display.width] = color

    time.sleep(0.03)
