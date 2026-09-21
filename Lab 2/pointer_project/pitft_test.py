import time
import math
import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789


# ============================================================
# PiTFT Setup
# ============================================================

cs_pin = digitalio.DigitalInOut(board.D5)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

BAUDRATE = 64000000

spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# After rotation, the visible screen is 240 x 135
width = disp.height
height = disp.width

rotation = 90


# ============================================================
# Backlight
# ============================================================

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# ============================================================
# Buttons
# Button A = GPIO23
# Button B = GPIO24
# Both are active LOW
# ============================================================

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)

buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB.switch_to_input(pull=digitalio.Pull.UP)


# ============================================================
# Pointer State
# ============================================================

# 0 = HOME
# 1 = SCHOOL
# 2 = GYM
# 3 = OUTDOOR

active_region = 0

# Each region has its own pointer length
pointer_lengths = [0, 0, 0, 0]

# Whether the currently active pointer is growing
pointer_growing = False

# Maximum pointer length
MAX_POINTER_LENGTH = 45

# Growth speed per frame
GROWTH_SPEED = 1.5


# ============================================================
# Region Settings
# ============================================================

region_colors = [
    (255, 180, 210),   # HOME - pink
    (150, 200, 255),   # SCHOOL - blue
    (160, 220, 160),   # GYM - green
    (255, 230, 150)    # OUTDOOR - yellow
]

region_names = [
    "HOME",
    "SCHOOL",
    "GYM",
    "OUTDOOR"
]


# ============================================================
# Pointer Directions
#
# HOME     -> upper-left
# SCHOOL   -> upper-right
# GYM      -> lower-left
# OUTDOOR  -> lower-right
# ============================================================

directions = [
    225,   # HOME
    315,   # SCHOOL
    135,   # GYM
    45     # OUTDOOR
]


# ============================================================
# Button State
# ============================================================

previous_A = True
previous_B = True


# ============================================================
# Main Loop
# ============================================================

while True:

    # --------------------------------------------------------
    # Create new frame
    # --------------------------------------------------------

    image = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(image)


    # --------------------------------------------------------
    # Draw four regions
    # --------------------------------------------------------

    center_x = width // 2
    center_y = height // 2

    # HOME - top left
    draw.rectangle(
        (0, 0, center_x, center_y),
        fill=region_colors[0]
    )

    # SCHOOL - top right
    draw.rectangle(
        (center_x, 0, width, center_y),
        fill=region_colors[1]
    )

    # GYM - bottom left
    draw.rectangle(
        (0, center_y, center_x, height),
        fill=region_colors[2]
    )

    # OUTDOOR - bottom right
    draw.rectangle(
        (center_x, center_y, width, height),
        fill=region_colors[3]
    )


    # --------------------------------------------------------
    # Highlight active region
    # --------------------------------------------------------

    border_width = 3

    if active_region == 0:
        draw.rectangle(
            (0, 0, center_x - 1, center_y - 1),
            outline=(255, 255, 255),
            width=border_width
        )

    elif active_region == 1:
        draw.rectangle(
            (center_x, 0, width - 1, center_y - 1),
            outline=(255, 255, 255),
            width=border_width
        )

    elif active_region == 2:
        draw.rectangle(
            (0, center_y, center_x - 1, height - 1),
            outline=(255, 255, 255),
            width=border_width
        )

    elif active_region == 3:
        draw.rectangle(
            (center_x, center_y, width - 1, height - 1),
            outline=(255, 255, 255),
            width=border_width
        )


    # --------------------------------------------------------
    # Draw all four pointers
    #
    # IMPORTANT:
    # Every pointer starts from the exact same center point:
    #
    # (120, 67)
    #
    # --------------------------------------------------------

    pointer_center_x = width // 2
    pointer_center_y = height // 2

    for i in range(4):

        length = pointer_lengths[i]

        if length <= 0:
            continue

        angle = math.radians(directions[i])

        end_x = (
            pointer_center_x
            + math.cos(angle) * length
        )

        end_y = (
            pointer_center_y
            + math.sin(angle) * length
        )

        # Pointer
        draw.line(
            (
                pointer_center_x,
                pointer_center_y,
                end_x,
                end_y
            ),
            fill=(0, 0, 0),
            width=3
        )


    # --------------------------------------------------------
    # Draw a small center point
    #
    # This makes it visually obvious that all pointers
    # originate from the exact same center.
    # --------------------------------------------------------

    center_radius = 3

    draw.ellipse(
        (
            pointer_center_x - center_radius,
            pointer_center_y - center_radius,
            pointer_center_x + center_radius,
            pointer_center_y + center_radius
        ),
        fill=(0, 0, 0)
    )


    # --------------------------------------------------------
    # Button A
    #
    # Press A:
    # Switch to the next region
    # Automatically stop current pointer
    # --------------------------------------------------------

    current_A = buttonA.value

    if previous_A and not current_A:

        active_region = (active_region + 1) % 4

        # Stop growing when switching region
        pointer_growing = False

        print(
            "Active region:",
            region_names[active_region]
        )

        time.sleep(0.15)

    previous_A = current_A


    # --------------------------------------------------------
    # Button B
    #
    # Press B:
    # Start / stop pointer growth
    #
    # Press 1 -> start
    # Press 2 -> stop
    # Press 3 -> continue
    # --------------------------------------------------------

    current_B = buttonB.value

    if previous_B and not current_B:

        pointer_growing = not pointer_growing

        if pointer_growing:

            print(
                "Pointer STARTED:",
                region_names[active_region]
            )

        else:

            print(
                "Pointer STOPPED:",
                region_names[active_region]
            )

        time.sleep(0.15)

    previous_B = current_B


    # --------------------------------------------------------
    # Grow active pointer
    # --------------------------------------------------------

    if pointer_growing:

        if pointer_lengths[active_region] < MAX_POINTER_LENGTH:

            pointer_lengths[active_region] += GROWTH_SPEED

            if pointer_lengths[active_region] > MAX_POINTER_LENGTH:

                pointer_lengths[active_region] = MAX_POINTER_LENGTH

        else:

            pointer_growing = False

            print(
                "Pointer reached maximum length:",
                region_names[active_region]
            )


    # --------------------------------------------------------
    # Send image to PiTFT
    # --------------------------------------------------------

    disp.image(image, rotation)

    time.sleep(0.03)
