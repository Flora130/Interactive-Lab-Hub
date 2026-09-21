
import time
import math
import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789


# ==========================================
# PiTFT configuration
# ==========================================

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

# Physical screen size after rotation
WIDTH = 240
HEIGHT = 135
ROTATION = 90


# ==========================================
# Backlight
# GPIO22
# ==========================================

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# ==========================================
# PiTFT Buttons
#
# Button A = GPIO23
# Button B = GPIO24
#
# Buttons are active LOW:
# Not pressed = True
# Pressed     = False
# ==========================================

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)

buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB.switch_to_input(pull=digitalio.Pull.UP)


# ==========================================
# Pointer state
# ==========================================

# Current active region
# 0 = HOME
# 1 = SCHOOL
# 2 = GYM
# 3 = OUTDOOR
active_region = 0


# Each region has its own pointer length
pointer_lengths = [0, 0, 0, 0]


# Whether the current pointer is growing
pointer_growing = False


# Maximum pointer length
MAX_POINTER_LENGTH = 45


# How fast the pointer grows
GROWTH_SPEED = 1.5


# ==========================================
# Pointer directions
#
# HOME     = 225 degrees
# SCHOOL   = 315 degrees
# GYM      = 135 degrees
# OUTDOOR  = 45 degrees
# ==========================================

directions = [
    225,
    315,
    135,
    45
]


# ==========================================
# Region colors
# ==========================================

region_colors = [
    (255, 180, 210),   # HOME - pink
    (150, 200, 255),   # SCHOOL - blue
    (160, 220, 160),   # GYM - green
    (255, 230, 150)    # OUTDOOR - yellow
]


# ==========================================
# Region names
# ==========================================

region_names = [
    "HOME",
    "SCHOOL",
    "GYM",
    "OUTDOOR"
]


# ==========================================
# Previous button states
#
# Used to detect a NEW button press.
# ==========================================

previous_A = True
previous_B = True


# ==========================================
# Screen drawing function
# ==========================================

def draw_screen():

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT)
    )

    draw = ImageDraw.Draw(image)


    # --------------------------------------
    # Four regions
    # --------------------------------------

    # HOME
    draw.rectangle(
        (0, 0, 119, 66),
        fill=region_colors[0]
    )

    # SCHOOL
    draw.rectangle(
        (120, 0, 239, 66),
        fill=region_colors[1]
    )

    # GYM
    draw.rectangle(
        (0, 67, 119, 134),
        fill=region_colors[2]
    )

    # OUTDOOR
    draw.rectangle(
        (120, 67, 239, 134),
        fill=region_colors[3]
    )


    # --------------------------------------
    # Region dividing lines
    # --------------------------------------

    draw.line(
        (120, 0, 120, 135),
        fill=(255, 255, 255),
        width=1
    )

    draw.line(
        (0, 67, 240, 67),
        fill=(255, 255, 255),
        width=1
    )


    # --------------------------------------
    # Center position of each region
    # --------------------------------------

    centers = [
        (60, 33),      # HOME
        (180, 33),     # SCHOOL
        (60, 101),     # GYM
        (180, 101)     # OUTDOOR
    ]


    # --------------------------------------
    # Draw all four pointers
    # --------------------------------------

    for i in range(4):

        length = pointer_lengths[i]

        # Don't draw a pointer if length is 0
        if length <= 0:
            continue


        cx, cy = centers[i]


        # Convert degrees to radians
        angle = math.radians(
            directions[i]
        )


        # Calculate pointer endpoint
        end_x = (
            cx
            + length * math.cos(angle)
        )

        end_y = (
            cy
            + length * math.sin(angle)
        )


        # ----------------------------------
        # Pointer line
        # ----------------------------------

        draw.line(
            (cx, cy, end_x, end_y),
            fill=(30, 30, 30),
            width=4
        )


        # ----------------------------------
        # Pointer tip
        # ----------------------------------

        draw.ellipse(
            (
                end_x - 3,
                end_y - 3,
                end_x + 3,
                end_y + 3
            ),
            fill=(30, 30, 30)
        )


    # --------------------------------------
    # Highlight active region
    # --------------------------------------

    if active_region == 0:

        draw.rectangle(
            (1, 1, 118, 65),
            outline=(255, 255, 255),
            width=2
        )

    elif active_region == 1:

        draw.rectangle(
            (121, 1, 238, 65),
            outline=(255, 255, 255),
            width=2
        )

    elif active_region == 2:

        draw.rectangle(
            (1, 68, 118, 133),
            outline=(255, 255, 255),
            width=2
        )

    elif active_region == 3:

        draw.rectangle(
            (121, 68, 238, 133),
            outline=(255, 255, 255),
            width=2
        )


    # --------------------------------------
    # Send image to PiTFT
    # --------------------------------------

    disp.image(
        image,
        ROTATION
    )


# ==========================================
# Main loop
# ==========================================

print("==========================================")
print("PiTFT Pointer started")
print("==========================================")
print("Button A: switch region")
print("Button B: start / stop pointer growth")
print("Press Ctrl+C to exit")
print("==========================================")


try:

    while True:


        # ==================================
        # BUTTON A
        #
        # One press = switch region
        # ==================================

        current_A = buttonA.value


        # Detect a NEW press:
        # previous = not pressed
        # current  = pressed

        if previous_A and not current_A:

            # Move to next region
            active_region = (
                active_region + 1
            ) % 4


            # Stop pointer growth
            # when switching regions
            pointer_growing = False


            print(
                "Active region:",
                region_names[active_region]
            )


            # Small debounce delay
            time.sleep(0.15)


        previous_A = current_A


        # ==================================
        # BUTTON B
        #
        # First press  = START
        # Second press = STOP
        # Third press  = START
        # ...
        # ==================================

        current_B = buttonB.value


        # Detect a NEW press

        if previous_B and not current_B:

            # Toggle growth state
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


            # Small debounce delay
            time.sleep(0.15)


        previous_B = current_B


        # ==================================
        # Grow the active pointer
        # ==================================

        if pointer_growing:

            if (
                pointer_lengths[active_region]
                < MAX_POINTER_LENGTH
            ):

                pointer_lengths[active_region] += (
                    GROWTH_SPEED
                )


                # Make sure we don't exceed max
                if (
                    pointer_lengths[active_region]
                    > MAX_POINTER_LENGTH
                ):

                    pointer_lengths[active_region] = (
                        MAX_POINTER_LENGTH
                    )


            else:

                # Automatically stop when
                # maximum length is reached
                pointer_growing = False

                print(
                    "Pointer reached maximum length:",
                    region_names[active_region]
                )


        # ==================================
        # Update display
        # ==================================

        draw_screen()


        # Small delay
        time.sleep(0.03)


except KeyboardInterrupt:

    print("\nStopping PiTFT Pointer...")


finally:

    # Turn off backlight when program exits
    backlight.value = False

    print("PiTFT Pointer stopped.")
