import network
from picographics import PEN_1BIT, PicoGraphics, DISPLAY_INKY_PACK
import pngdec
import time
import urequests

from secrets import PASSWORD, SSID, URL


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


def setup_display():
    display = PicoGraphics(display=DISPLAY_INKY_PACK,  pen_type=PEN_1BIT)
    display.set_update_speed(0)
    return display


def fetch_and_display(display, pngdecInstance):
    print("Fetching image...")
    width, height = display.get_bounds()
    url = f"{URL}?width={width}&height={height}"
    print(url)
    while True:
        try:
            now = time.localtime()
            print("Time: {}:{}:{}".format(now[3], now[4], now[5]))
            if time.time() % 60 != 0:
                print("Waiting for the right time...")
                time.sleep(1)
                continue
            print("right time {}:{}:{}".format(now[3], now[4], now[5]))
            response = urequests.get(url)
            if response.status_code == 200:
                print("Image received, displaying...")
                display_png(display, pngdecInstance, response.content)
            else:
                print("Failed to fetch image:", response.status_code)
            response.close()
            print("Updated, Waiting for the right time...")
            time.sleep(1)
        except Exception as e:
            print("Error fetching image:", e)


def display_png(display, pngdecInstance, path):
    with open(path, "rb") as f:
        pngdecInstance.open_RAM(f.read())
    pngdecInstance.decode(0, 0)
    display.update()


def main():
    display = setup_display()
    connect_wifi()
    pngdecInstance = pngdec.PNG(display)
    fetch_and_display(display, pngdecInstance)


main()
