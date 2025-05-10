
from src.image_renderer.image_renderer import ImageRendererAbstract


class DisplayConfig:
    def __init__(self, display: int, pen_type: int, image_renderer_cls: type[ImageRendererAbstract] | None = None):
        self.display = display
        self.pen_type = pen_type
        self.image_renderer_cls = image_renderer_cls
