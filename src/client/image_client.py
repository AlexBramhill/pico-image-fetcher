import urequests
import sys
from src.enums.image_types import IMAGE_TYPE
from secrets import URL


class ImageClientGetConfig:
    def __init__(self, image_type, image_rotation, width, height):
        self.width: int = width
        self.height: int = height
        self.image_type: int = image_type
        self.image_rotation: int = image_rotation


class ImageClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ImageClient, cls).__new__(cls)
        return cls._instance

    def _make_request(self, width: int, height: int, image_format: str, image_rotation=0, timeout_in_seconds=30):
        url = URL
        params = []

        params.append(f"width={width}")
        params.append(f"height={height}")
        params.append(f"format={image_format}")
        params.append(f"rotation={image_rotation}")

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
        elif (image_type == IMAGE_TYPE.BMP):
            return "bmp"
        elif (image_type == IMAGE_TYPE.BMP_RAW):
            return "bmp_raw"
        else:
            raise ValueError(f"Unsupported image type: {image_type}")

    def get(self, config: ImageClientGetConfig):
        try:
            return self._make_request(
                config.width, config.height, self._get_image_type_value(config.image_type), image_rotation=config.image_rotation)

        except Exception as e:
            print("ImageClient get error:", e, file=sys.stderr)
            return None
