import config

from submodules.event_loop import EventLoop, TaskSchedulerBuilder, Task
from submodules.wifi_manager import WiFiManager
from submodules.clock_service import ClockService

from src.client.image_client import ImageClient
from src.interaction_controller import InteractionController


class App:
    def __init__(self):
        print("Starting up")

        self.clock_service = ClockService()
        self.wifi_manager = WiFiManager()
        self.image_client = ImageClient()
        self.display = config.DISPLAY_CLASS(
            max_update_speed_in_ms=config.DISPLAY_MAX_UPDATE_SPEED_MS,
            hard_refresh_interval=config.DISPLAY_HARD_REFRESH_INTERVAL,
        )

        self.interaction_controller = InteractionController(
            wifi_manager=self.wifi_manager,
            image_client=self.image_client,
            display=self.display,
            clock_service=self.clock_service,
        )

        tasks = self._get_tasks()
        self.scheduler = TaskSchedulerBuilder().add_tasks(tasks).build()
        self.event_loop = EventLoop(self.scheduler)
        print("App initialized")

    def _get_tasks(self) -> list[Task]:
        return [
            Task(
                name="Fetch and render page",
                callback=self.interaction_controller.fetch_and_render_page,
                get_ms_to_next_run=lambda: config.DISPLAY_MAX_UPDATE_SPEED_MS,
                should_run_once=False,
            )
        ]

    def run(self):
        self.event_loop.start()
