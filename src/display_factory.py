from picographics import PicoGraphics

from src.display_config import DisplayConfig


class DisplayFactory:
    _instance = None

    @staticmethod
    def get_instance(config: DisplayConfig) -> PicoGraphics:
        if DisplayFactory._instance is None:
            DisplayFactory._instance = PicoGraphics(
                config.display, config.pen_type)

            try:
                DisplayFactory._instance.set_update_speed(2)
            except ValueError:
                print("Display does not support set_update_speed, skipping")

        return DisplayFactory._instance
