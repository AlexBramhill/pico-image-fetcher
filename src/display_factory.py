from picographics import PEN_1BIT, PicoGraphics, DISPLAY_INKY_PACK


def init():
    display = PicoGraphics(display=DISPLAY_INKY_PACK,  pen_type=PEN_1BIT)
    display.set_update_speed(0)
    return display
