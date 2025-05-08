from picographics import PicoGraphics

from display_config import DisplayConfig
from image_renderer.image_renderer import ImageRendererAbstract


class DisplayController:
    def __init__(self, config: DisplayConfig, image_renderer_cls: type[ImageRendererAbstract] | None = None):
        self._config = config
        self._display = PicoGraphics(config.display, config.pen_type)
        if (image_renderer_cls is not None):
            self._image_renderer = image_renderer_cls(self._display)

    def get_image_renderer(self) -> ImageRendererAbstract | None:
        if (not hasattr(self, "_image_renderer")):
            raise ValueError(
                "Image renderer class is not set in the configuration.")
        return self._image_renderer
