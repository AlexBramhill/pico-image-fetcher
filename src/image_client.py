import time
import urequests
import sys
from src.image_renderer.image_renderer import ImageRendererAbstract
from secrets import URL


class ImageClientGetConfig:
    def __init__(self, width=None, height=None, image_format=None):
        self.width = width
        self.height = height
        self.image_format = image_format


class ImageClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ImageClient, cls).__new__(cls)
        return cls._instance

    def _make_request(self, width=None, height=None, image_format=None):
        url = URL
        params = []

        if width is not None:
            params.append(f"width={width}")
        if height is not None:
            params.append(f"height={height}")
        if image_format is not None:
            params.append(f"format={image_format}")

        if params:
            url += "?" + "&".join(params)

        response = urequests.get(url)
        if not response:
            raise ValueError("Failed to get response from server.")

        return response

    def get(self, config: ImageClientGetConfig):
        try:
            response = self._make_request(
                config.width, config.height, config.image_format)

            content = response.content
            response.close()
            return content
        except Exception as e:
            print("ImageClient get error:", e, file=sys.stderr)
        return None

    def get_time_from_http_request_header(self):
        response = self._make_request()

        date_str = response.headers.get("Date")
        if date_str:
            # Example: 'Fri, 08 May 2025 12:34:56 GMT'
            return time.strptime(
                date_str, "%a, %d %b %Y %H:%M:%S GMT")
        response.close()
