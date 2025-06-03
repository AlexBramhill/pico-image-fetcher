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
                run_every_x_ms=self.display.get_next_update_time(
                ) if self.display.get_next_update_time() else 0,
                should_run_once=False,
            )
        ]

    def run(self):
        # Start the event loop here
        self.event_loop.start()
