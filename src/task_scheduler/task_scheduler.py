import time
from src.tasks.task import Task


class TaskScheduler:
    def __init__(self, tasks=[]):
        self.tasks = tasks

    def pop_overdue_task(self):
        now = time.ticks_ms()
        overdue_tasks = [
            task for task in self.tasks if task.next_run_in_epoch is None or task.next_run_in_epoch <= now]
        if overdue_tasks:
            oldest_task = min(
                overdue_tasks, key=lambda t: t.next_run_in_epoch if t.next_run_in_epoch is not None else float('-inf'))
            self.tasks.remove(oldest_task)
            return oldest_task
        else:
            return None

    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("task must be an instance of Task")
        self.tasks.append(task)
