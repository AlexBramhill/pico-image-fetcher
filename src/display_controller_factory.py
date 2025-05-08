from picographics import PicoGraphics

from display_config import DisplayConfig
from display_controller import DisplayController
from image_renderer.image_renderer import ImageRendererAbstract


class DisplayControllerFactory:
    _instance = None

    @staticmethod
    def get_instance(display_config: DisplayConfig, image_renderer_cls: type[ImageRendererAbstract] | None = None) -> DisplayController:
        if DisplayControllerFactory._instance is None:
            DisplayControllerFactory._instance = DisplayController(
                display_config, image_renderer_cls)
        return DisplayControllerFactory._instance
