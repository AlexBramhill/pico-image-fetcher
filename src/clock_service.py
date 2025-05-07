import machine


def set_time(new_time):
    rtc = machine.RTC()
    print('Setting time')
    print(new_time)
    # (year, month, day, weekday, hours, minutes, seconds, subseconds)
    rtc.datetime((new_time["year"], new_time["month"],
                  new_time["day"], 0, new_time["hour"], new_time["minute"], new_time["seconds"], new_time["subseconds"]))
    print('time set')
