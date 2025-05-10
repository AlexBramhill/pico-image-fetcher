from picographics import PEN_1BIT, DISPLAY_INKY_PACK


from src.image_client import ImageClient
from src.image_renderer.png_renderer import PngRenderer
from src.interaction_controller import InteractionController
from secrets import URL
from src.wifi_manager import WiFiManager
from src.cron_scheduler import CronScheduler
from src.display_factory import DisplayConfig, DisplayFactory


def main():
    print("Starting up")

    wifi_service = WiFiManager()
    scheduler = CronScheduler()
    image_client = ImageClient()
    inky_display_config = DisplayConfig(
        display=DISPLAY_INKY_PACK, pen_type=PEN_1BIT)
    display = DisplayFactory.get_instance(inky_display_config)
    image_renderer = PngRenderer(display)

    interaction_controller = InteractionController(
        wifi_manager=wifi_service,
        image_client=image_client,
        display=display,
        image_renderer=image_renderer,
    )

    print("Initailisation complete")

    interaction_controller.fetch_and_display_image()

    scheduler.add_schedule(
        lambda: interaction_controller.fetch_and_display_image(),
        "*/1 * * * * *"
    ).run_scheduler()

main()
