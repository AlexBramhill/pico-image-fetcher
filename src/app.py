import config
from src.image_renderer.factories.image_renderer_factory import ImageRendererFactory
from src.display.configs.display_configs import display_configs
from src.display.factories.display_factory import DisplayFactory

from src.clock.clock_service import ClockService
from src.client.image_client import ImageClient
from src.interaction_controller import InteractionController
from src.wifi.wifi_manager import WiFiManager
from src.event_loop.event_loop import EventLoop
from src.task_dispatcher.task_dispatcher import TaskDispatcher
from src.task_scheduler.task_scheduler_builder import TaskSchedulerBuilder
from src.tasks.task import Task


class App:
    def __init__(self):
        print("Starting up")

        self.clock_service = ClockService()
        self.wifi_manager = WiFiManager()
        self.image_client = ImageClient()

        self.display = DisplayFactory.create(
            display_configs[config.DISPLAY_TO_USE](config.IMAGE_FORMAT_TO_USE)
        )

        self.image_renderer = ImageRendererFactory.create_renderer(
            display=self.display,
            image_type=config.IMAGE_FORMAT_TO_USE,
        )

        self.interaction_controller = InteractionController(
            wifi_manager=self.wifi_manager,
            image_client=self.image_client,
            display=self.display,
            image_renderer=self.image_renderer,
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
                get_ms_to_next_run=self._get_last_run,
                should_run_once=False,
            )
        ]

    def _get_last_run(self):
        print("--Getting last run time")
        print("--Next run time:", self.display.get_ms_until_next_update_available())
        update_time = 0

        return max(update_time, self.display.get_ms_until_next_update_available(
            # type: ignore
        )) if self.display.get_ms_until_next_update_available() else update_time

    def run(self):
        # Start the event loop here
        self.event_loop.start()
