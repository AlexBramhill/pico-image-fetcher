from src.display.abstract.display_abstract import DisplayAbstract
from src.clock.clock_service import ClockService
from src.client.image_client import ImageClient, ImageClientGetConfig
from src.image_renderer.abstract.image_renderer_abstract import ImageRendererAbstract
from src.wifi.wifi_manager import WiFiManager


class InteractionController:
    def __init__(self,
                 wifi_manager: WiFiManager,
                 image_client: ImageClient,
                 display: DisplayAbstract,
                 image_renderer: ImageRendererAbstract,
                 clock_service: ClockService):
        self._wifi_manager = wifi_manager
        self._image_client = image_client
        self._display = display
        self._image_renderer = image_renderer
        self._clock_service = clock_service

    def fetch_and_render_page(self):
        try:
            if (self._wifi_manager.is_connected() is False):
                self._wifi_manager.connect()

            width, height = self._display.get_bounds()
            config = ImageClientGetConfig(
                width=width,
                height=height,
                image_type=self._image_renderer.get_image_type(),
                image_rotation=self._display.get_default_rotation(),
            )

            response = self._image_client.get(config)

            if response is None:
                raise ValueError("Failed to get image from server.")

            if not (100 <= response.status_code <= 299):
                raise ValueError(
                    f"Failed to fetch image, status code: {response.status_code}")

            if self._clock_service.is_time_set() is False:
                self._clock_service.set_time_from_header(response.headers)

            self._image_renderer.display_image_from_bytes(response.content)
        except Exception as e:
            print("Error fetching and displaying image:", e)
