import utime


class CronScheduler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CronScheduler, cls).__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self):
        if not self._initialised:
            self._tasks = []
            self._initialised = True

    def _parse_cron_field(self, field, min_val, max_val):
        if field == '*':
            return list(range(min_val, max_val + 1))
        elif ',' in field:
            return [int(x) for x in field.split(',')]
        elif '-' in field:
            start, end = map(int, field.split('-'))
            return list(range(start, end + 1))
        elif '/' in field:
            base, step = field.split('/')
            if base == '*':
                return list(range(min_val, max_val + 1, int(step)))
            else:
                start, end = map(int, base.split('-'))
                return list(range(start, end + 1, int(step)))
        else:
            return [int(field)]

    def _matches_cron(self, now, cron_parts):
        second, minute, hour, day, month, weekday = cron_parts
        return (
            now[5] in second and
            now[4] in minute and
            now[3] in hour and
            now[2] in day and
            now[1] in month and
            now[6] in weekday
        )

    def add_scheduled_job(self, callback, cron_expression, fail_silently=False, display_focused=False, is_display_ready_to_update=None):
        fields = cron_expression.strip().split()
        if len(fields) != 6:
            raise ValueError(
                "Expected 6 fields: sec min hour day month weekday")

        parsed_cron_values = [
            self._parse_cron_field(fields[0], 0, 59),
            self._parse_cron_field(fields[1], 0, 59),
            self._parse_cron_field(fields[2], 0, 23),
            self._parse_cron_field(fields[3], 1, 31),
            self._parse_cron_field(fields[4], 1, 12),
            self._parse_cron_field(fields[5], 0, 6),
        ]

        self._tasks.append((callback, parsed_cron_values, fail_silently,
                           display_focused, is_display_ready_to_update))
        return self

    def run_scheduler(self):
        last_time = None
        while True:
            now = utime.localtime()
            if now != last_time:
                for callback, cron_value, fail_silently, display_focused, is_display_ready_to_update in self._tasks:
                    if display_focused and (is_display_ready_to_update() is not True):
                        print("Display not ready, skipping scheduled task")
                        continue

                    if self._matches_cron(now, cron_value):
                        print("Running a scheduled task")
                        if (not fail_silently):
                            callback()
                        else:
                            try:
                                callback()
                            except Exception as e:
                                print("Error in scheduled task:", e)
                last_time = now
            utime.sleep(1)
