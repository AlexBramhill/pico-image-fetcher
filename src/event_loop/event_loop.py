import time

from src.task_scheduler.task_scheduler import TaskScheduler
from src.task_dispatcher.task_dispatcher import TaskDispatcher


class EventLoop:
    def __init__(self, scheduler: TaskScheduler):
        self.scheduler = scheduler
        self.dispatcher = TaskDispatcher(scheduler)
        self._running = False

    def start(self):
        self._running = True
        while self._running:
            self.dispatcher.dispatch()

    def stop(self):
        self._running = False
