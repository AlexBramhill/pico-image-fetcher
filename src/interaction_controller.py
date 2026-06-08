import config

from submodules.displays.abstract.display_base import DisplayBase
from submodules.clock_service.clock_service import ClockService
from src.client.image_client import ImageClient, ImageClientGetConfig
from submodules.wifi_manager import WiFiManager
from secrets import SSID, PASSWORD


class InteractionController:
    def __init__(self,
                 wifi_manager: WiFiManager,
                 image_client: ImageClient,
                 display: DisplayBase,
                 clock_service: ClockService):
        self._wifi_manager = wifi_manager
        self._image_client = image_client
        self._display = display
        self._clock_service = clock_service

    def fetch_and_render_page(self):
        try:
            if not self._wifi_manager.is_connected():
                self._wifi_manager.connect(ssid=SSID, password=PASSWORD)

            request_config = ImageClientGetConfig(
                width=config.IMAGE_WIDTH,
                height=config.IMAGE_HEIGHT,
                image_type=config.IMAGE_FORMAT,
                image_rotation=config.IMAGE_ROTATION,
                colour_profile=config.COLOUR_PROFILE_TO_USE,
            )

            response = self._image_client.get(request_config)

            if response is None:
                raise ValueError("Failed to get image from server.")

            if not (100 <= response.status_code <= 299):
                raise ValueError(
                    f"Failed to fetch image, status code: {response.status_code}")

            if not self._clock_service.is_time_set():
                self._clock_service.set_time_from_header(response.headers)

            self._display.draw_image(response.content, config.IMAGE_FORMAT, config.COLOUR_PROFILE_TO_USE)
        except Exception as e:
            print("Error fetching and displaying image:", e)
