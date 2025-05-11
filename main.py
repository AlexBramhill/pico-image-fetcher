from picographics import PEN_1BIT, DISPLAY_INKY_PACK

import secrets

from src.clock_service import ClockService
from src.display_configs import get_display_config
from src.image_client import ImageClient
from src.image_renderer.png_renderer import PngRenderer
from src.image_renderer.jpeg_renderer import JpegRenderer
from src.interaction_controller import InteractionController
from src.wifi_manager import WiFiManager
from src.cron_scheduler import CronScheduler
from src.display_factory import DisplayFactory


def main():
    print("Starting up")


clock_service = ClockService()
wifi_manager = WiFiManager()
scheduler = CronScheduler()
image_client = ImageClient()
display = DisplayFactory.get_instance(get_display_config(
    secrets.DISPLAY_TYPE
))

image_renderer = PngRenderer(
    display) if secrets.IMAGE_RENDERER == "png" else JpegRenderer(display)

interaction_controller = InteractionController(
    wifi_manager=wifi_manager,
    image_client=image_client,
    display=display,
    image_renderer=image_renderer,
    clock_service=clock_service,
)

print("Dependency initialisation complete")

print("Initial fetches")
interaction_controller.fetch_and_render_page()
print("Initial fetches complete")

scheduler.add_scheduled_job(
    lambda: interaction_controller.fetch_and_render_page(),
    "0 * * * * *",
    fail_silently=True,
).run_scheduler()


main()
