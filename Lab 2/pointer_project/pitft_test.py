import time
import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789

# -----------------------------
# PiTFT configuration
# -----------------------------
cs_pin = digitalio.DigitalInOut(board.D5)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=64000000,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# PiTFT is physically 240 x 135 after rotation
width = 240
height = 135
rotation = 90

# -----------------------------
# Backlight
# -----------------------------
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# -----------------------------
# Create test image
# -----------------------------
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)

# Four regions
draw.rectangle((0, 0, 119, 66), fill=(255, 180, 210))       # pink
draw.rectangle((120, 0, 239, 66), fill=(150, 200, 255))     # blue
draw.rectangle((0, 67, 119, 134), fill=(160, 220, 160))     # green
draw.rectangle((120, 67, 239, 134), fill=(255, 230, 150))   # yellow

# Draw borders
draw.line((120, 0, 120, 135), fill=(255, 255, 255), width=1)
draw.line((0, 67, 240, 67), fill=(255, 255, 255), width=1)

# Send image to PiTFT
disp.image(image, rotation)

print("PiTFT test image displayed.")
print("Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    backlight.value = False
