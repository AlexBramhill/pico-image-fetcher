from picographics import DISPLAY_INKY_PACK, DISPLAY_PICO_DISPLAY_2, PEN_1BIT, PEN_P8
from src.display_config import DisplayConfig


inky_display_config = DisplayConfig(
    display=DISPLAY_INKY_PACK, pen_type=PEN_1BIT)

display_pack_2 = DisplayConfig(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P8)


def get_display_config(display_type):
    if display_type == "inky":
        return inky_display_config
    elif display_type == "pico_display":
        return display_pack_2
    else:
        raise ValueError(f"Unknown display type: {display_type}")
