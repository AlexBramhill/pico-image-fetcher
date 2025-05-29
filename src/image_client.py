import time
import urequests
import sys
from src.image_renderer.image_types import IMAGE_TYPE
from src.image_renderer.image_renderer import ImageRendererAbstract
from secrets import URL


class ImageClientGetConfig:
    def __init__(self, image_type, width, height):
        self.width = width
        self.height = height
        self.image_type = image_type


class ImageClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ImageClient, cls).__new__(cls)
        return cls._instance

    def _make_request(self, width=None, height=None, image_format=None, timeout_in_seconds=30):
        url = URL
        params = []

        params.append(f"width={width}")
        params.append(f"height={height}")
        params.append(f"format={image_format}")

        if params:
            url += "?" + "&".join(params)

        print("Making request to URL:", url)
        response = urequests.get(url, timeout=timeout_in_seconds)
        if not response:
            raise ValueError("Failed to get response from server.")

        return response

    def _get_image_type_value(self, image_type: int):
        if (image_type == IMAGE_TYPE.PNG):
            return "png"
        elif (image_type == IMAGE_TYPE.JPG):
            return "jpg"
        else:
            raise ValueError(f"Unsupported image type: {image_type}")

    def get(self, config: ImageClientGetConfig):
        try:
            return self._make_request(
                config.width, config.height, self._get_image_type_value(config.image_type))

        except Exception as e:
            print("ImageClient get error:", e, file=sys.stderr)
            return None
