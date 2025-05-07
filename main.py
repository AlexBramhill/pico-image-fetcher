import network
from picographics import PEN_1BIT, PicoGraphics, DISPLAY_INKY_PACK
import pngdec
import time
import urequests

import display_factory
from secrets import URL
import wifi_service


def fetch_and_display_job(display, pngdecInstance):
    while True:
        now = time.localtime()
        print("Time: {}:{}:{}".format(now[3], now[4], now[5]))
        if time.time() % 60 != 0:
            print("Waiting for the right time...")
            time.sleep(1)
            continue
        print("right time {}:{}:{}".format(now[3], now[4], now[5]))
        fetch_and_display_image(display, pngdecInstance)
        print("Updated, Waiting for the right time...")
        time.sleep(1)


def fetch_and_display_image(display, pngdecInstance):
    width, height = display.get_bounds()
    url = f"{URL}?width={width}&height={height}&format=png"

    print("Fetching image...")
    print(url)
    try:
        response = urequests.get(url)
        date_header = response.headers.get("Date", None)
        if date_header:
            print("Date from header:", date_header)
            try:
            parsed_date = time.strptime(
                date_header, "%a, %d %b %Y %H:%M:%S %Z")
            print("Parsed date:", parsed_date)
            except Exception as e:
            print("Error parsing date:", e)
        print(f"{response}")
    except Exception as e:
        print("Error fetching image:", e)
        return
    print("Response code:", response.status_code)
    if response.status_code == 200:
        print("Image received, displaying...")
        display_png(display, pngdecInstance, response.content)
    else:
        print("Failed to fetch image:", response.status_code)
    response.close()


def display_png_from_file(display, pngdecInstance, path):
    with open(path, "rb") as f:
        pngdecInstance.open_RAM(f.read())
        pngdecInstance.decode(0, 0)
    display.update()


def display_png(display, pngdecInstance, image_bytes):
    pngdecInstance.open_RAM(image_bytes)
    pngdecInstance.decode(0, 0)
    display.update()


def main():
    display = display_factory.init()
    pngdecInstance = pngdec.PNG(display)
    wifi_service.connect_wifi()
    # initial load
    fetch_and_display_image(display, pngdecInstance)

    fetch_and_display_job(display, pngdecInstance)


main()
