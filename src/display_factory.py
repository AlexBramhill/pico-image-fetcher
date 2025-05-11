from picographics import PicoGraphics

from src.display_config import DisplayConfig


class DisplayFactory:
    _instance = None

    @staticmethod
    def get_instance(config: DisplayConfig) -> PicoGraphics:
        if DisplayFactory._instance is None:
            DisplayFactory._instance = PicoGraphics(
                config.display, config.pen_type)
            DisplayFactory._instance.set_update_speed(1)
        return DisplayFactory._instance
