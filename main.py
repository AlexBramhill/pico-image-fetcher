import config
from src.image_renderer.factories.image_renderer_factory import ImageRendererFactory
from src.display.configs.display_configs import display_configs
from src.display.factories.display_factory import DisplayFactory
import secrets

from src.clock.clock_service import ClockService
from src.client.image_client import ImageClient
from src.interaction_controller import InteractionController
from src.wifi.wifi_manager import WiFiManager
from src.cron_scheduler import CronScheduler


def main():
    print("Starting up")

    clock_service = ClockService()
    wifi_manager = WiFiManager()
    scheduler = CronScheduler()
    image_client = ImageClient()

    display = DisplayFactory.create(
        display_configs[config.DISPLAY_TO_USE](config.IMAGE_FORMAT_TO_USE))

    image_renderer = ImageRendererFactory.create_renderer(
        display=display,
        image_type=config.IMAGE_FORMAT_TO_USE,
    )
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
        run_as_fast_as_possible=True,
        fail_silently=True,
        display_focused=True,
        is_display_ready_to_update=lambda: display.is_ready_to_update(),

    ).run_scheduler()


main()
