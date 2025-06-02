import machine

from src.helpers.month_map import MONTH_MAP


class ClockService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ClockService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'rtc'):
            self.rtc = machine.RTC()
            self._rtc_initialised = False

    def set_time_from_header(self, request_header):
        date = request_header.get("Date")
        if not date:
            raise ValueError("No Date header in response")

        date_without_day = date.split(", ")[1]
        split_date = date_without_day.split(" ")

        rtc_formatted_date = {
            "year": int(split_date[2]),
            "month": int(MONTH_MAP[split_date[1]]),
            "day": int(split_date[0]),
            "hour": int(split_date[3].split(":")[0]),
            "minute": int(split_date[3].split(":")[1]),
            "seconds": int(split_date[3].split(":")[2]),
            "subseconds": 59
        }

        self.set_time(rtc_formatted_date)

    def set_time(self, new_time):
        self.rtc.datetime((new_time["year"], new_time["month"],
                           new_time["day"], 0, new_time["hour"], new_time["minute"], new_time["seconds"], new_time["subseconds"]))
        self._rtc_initialised = True
        print(f'RTC time set to: {self.rtc.datetime()}')

    def is_time_set(self):
        return self._rtc_initialised
