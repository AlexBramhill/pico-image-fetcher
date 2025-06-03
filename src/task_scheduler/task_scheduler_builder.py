from src.task_scheduler.task_scheduler import TaskScheduler
from src.tasks.task import Task


class TaskSchedulerBuilder:
    def __init__(self):
        self._tasks: list[Task] = []

    def add_task(self, task: Task):
        """
        Add a task to the task scheduler.
        :param task: An instance of TaskAbstract to be added.
        """
        if not isinstance(task, Task):
            raise TypeError("task must be an instance of TaskAbstract")
        self._tasks.append(task)
        return self

    def add_tasks(self, tasks: list[Task]):

        for task in tasks:
            self.add_task(task)
        return self

    def build(self):
        """
        Build and return the task scheduler.
        :return: The configured TaskScheduler instance.
        """
        return TaskScheduler(self._tasks)
