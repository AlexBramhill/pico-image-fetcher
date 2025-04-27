import network
import time

from secrets import PASSWORD, SSID


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to Wi-Fi...", end="")
    while not wlan.isconnected():
        time.sleep(0.5)
        print(".", end="")
    print("\nConnected to Wi-Fi!")
    print("IP:", wlan.ifconfig()[0])
