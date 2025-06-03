import time
from src.task_scheduler.task_scheduler import TaskScheduler


class TaskDispatcher:
    def __init__(self, scheduler: TaskScheduler):
        self.scheduler = scheduler

    def dispatch(self):
        task_generator = self.scheduler.yield_most_overdue_task()
        task = next(task_generator)

        if task is None:
            print("No tasks to run.")
            return

        try:
            task.run()
        except Exception as e:
            print(f"Error in task {task.name}: {e}")

        # Avoids missing scheduled tasks, but means an infinite backlog can occur
        if not task.should_run_once:
            now = time.ticks_ms()

            last_run = task.last_run_in_epoch if task.last_run_in_epoch is not None else now
            task.next_run_in_epoch = time.ticks_add(
                last_run, task.run_every_x_ms)
            task.last_run_in_epoch = now

            self.scheduler.add_task(task)
