class Task:
    def __init__(self, name, callback, run_every_x_ms, should_run_once=False):
        self.name = name
        self._last_run_in_epoch: int | None = None
        self._next_run_in_epoch: int | None = None
        self.callback = callback
        self.run_every_x_ms = run_every_x_ms
        self.should_run_once = should_run_once

    def run(self):
        self.callback()

    @property
    def last_run_in_epoch(self):
        return self._last_run_in_epoch

    @last_run_in_epoch.setter
    def last_run_in_epoch(self, value):
        self._last_run_in_epoch = value

    @property
    def next_run_in_epoch(self):
        return self._next_run_in_epoch

    @next_run_in_epoch.setter
    def next_run_in_epoch(self, value):
        self._next_run_in_epoch = value
