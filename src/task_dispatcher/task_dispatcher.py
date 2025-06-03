import time
from src.task_scheduler.task_scheduler import TaskScheduler


class TaskDispatcher:
    def __init__(self, scheduler: TaskScheduler):
        self.scheduler = scheduler

    def dispatch(self):
        task_generator = self.scheduler.yield_most_overdue_task()
        task = next(task_generator)

        if task is None:
            return

        try:
            task.run()
        except Exception as e:
            print(f"Error in task {task.name}: {e}")

        if not task.should_run_once:
            now = time.ticks_ms()

            last_run = task.last_run_in_epoch if task.last_run_in_epoch is not None else now
            print(
                f"Task {task.name} previous last run at {task.last_run_in_epoch}, now at {last_run}")
            print(
                f"Task {task.name} next run in {task.get_ms_to_next_run()} ms")
            task.next_run_in_epoch = last_run + task.get_ms_to_next_run()
            print(f"Task {task.name} next run at {task.next_run_in_epoch}")
            task.last_run_in_epoch = now
            print(f"Task {task.name} last run at {task.last_run_in_epoch}")

            print("Adding task back to the scheduler")
            self.scheduler.add_task(task)
            print(f"Task {task.name} added back to the scheduler")
