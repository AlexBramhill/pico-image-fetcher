from picographics import PicoGraphics
from src.image_client import ImageClient, ImageClientGetConfig
from src.image_renderer.image_renderer import ImageRendererAbstract
from src.wifi_manager import WiFiManager


class InteractionController:
    def __init__(self, wifi_manager: WiFiManager, image_client: ImageClient, display: PicoGraphics, image_renderer: ImageRendererAbstract):
        self._wifi_manager = wifi_manager
        self._image_client = image_client
        self._display = display
        self._image_renderer = image_renderer

    def fetch_and_display_image(self):
        try:
            if (self._wifi_manager.is_connected() is False):
                self._wifi_manager.connect()

            width, height = self._display.get_bounds()
            config = ImageClientGetConfig(
                width=width,
                height=height,
                image_format=self._image_renderer.get_required_file_format(),
            )

            content = self._image_client.get(config)

            if content is None:
                raise ValueError("Failed to get image from server.")

            self._image_renderer.display_image_from_bytes(content)
        except Exception as e:
            print("Error fetching and displaying image:", e)
