import urequests
import sys
from src.enums.image_types import IMAGE_TYPE
from src.enums.colour_profiles import COLOUR_PROFILE
from secrets import URL


class ImageClientGetConfig:
    def __init__(self, image_type, image_rotation, colour_profile, width, height):
        self.width: int = width
        self.height: int = height
        self.image_type: int = image_type
        self.image_rotation: int = image_rotation
        self.colour_profile: int = colour_profile


class ImageClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ImageClient, cls).__new__(cls)
        return cls._instance

    def _make_request(self, width: int, height: int, image_format: str, colour_profile: str, image_rotation=0, timeout_in_seconds=30):
        url = URL
        params = []

        params.append(f"width={width}")
        params.append(f"height={height}")
        params.append(f"format={image_format}")
        params.append(f"colour_profile={colour_profile}")
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

    def _get_colour_profile_value(self, colour_profile: int):
        if colour_profile == COLOUR_PROFILE.ONE_BIT:
            return "one_bit"
        elif colour_profile == COLOUR_PROFILE.TWO_BIT:
            return "two_bit"
        elif colour_profile == COLOUR_PROFILE.FOUR_BIT_PALETTE:
            return "four_bit_palette"
        elif colour_profile == COLOUR_PROFILE.EIGHT_BIT_PALETTE:
            return "eight_bit_palette"
        elif colour_profile == COLOUR_PROFILE.RGB332:
            return "rgb332"
        elif colour_profile == COLOUR_PROFILE.RGB565:
            return "rgb565"
        elif colour_profile == COLOUR_PROFILE.RGB888:
            return "rgb888"
        else:
            raise ValueError(f"Unsupported colour profile: {colour_profile}")

    def get(self, config: ImageClientGetConfig):
        try:
            return self._make_request(
                config.width, config.height, self._get_image_type_value(config.image_type), self._get_colour_profile_value(config.colour_profile), image_rotation=config.image_rotation)

        except Exception as e:
            print("ImageClient get error:", e, file=sys.stderr)
            return None
