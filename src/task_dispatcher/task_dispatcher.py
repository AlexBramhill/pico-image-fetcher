import time
from src.task_scheduler.task_scheduler import TaskScheduler


class TaskDispatcher:
    def __init__(self, scheduler: TaskScheduler):
        self._scheduler = scheduler

    def dispatch(self):
        task = self._scheduler.pop_overdue_task()
        if task is None:
            return

        try:
            print(f"Running task: {task.name}")
            task.run()
        except Exception as e:
            print(f"Error in task {task.name}: {e}")

        if not task.should_run_once:
            now = time.ticks_ms()
            last_run = task.last_run_in_epoch if task.last_run_in_epoch is not None else now
            task.next_run_in_epoch = now + task.get_ms_to_next_run()
            task.last_run_in_epoch = last_run
            self._scheduler.add_task(task)
