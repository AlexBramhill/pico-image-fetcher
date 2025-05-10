from picographics import PicoGraphics

from src.display_config import DisplayConfig
from src.image_renderer.image_renderer import ImageRendererAbstract


class DisplayFactory:
    _instance = None

    @staticmethod
    def get_instance(config: DisplayConfig) -> PicoGraphics:
        if DisplayFactory._instance is None:
            DisplayFactory._instance = PicoGraphics(
                config.display, config.pen_type)
        return DisplayFactory._instance
