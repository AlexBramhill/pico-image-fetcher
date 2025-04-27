import network
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import jpegdec
import time
import urequests

from secrets import PASSWORD, SSID, URL



def setup_display():
    display = PicoGraphics(display=DISPLAY_INKY_PACK)
    display.set_update_speed(0)
    return display


def setup_jpeg(display):
    jpeg = jpegdec.JPEG(display)
    return jpeg


def display_image(display, jpeg, bytearray_data):
    print(bytearray_data)
    jpeg.open_RAM(bytearray_data)
    jpeg.decode(0, 0, dither=False)
    display.update()


def fetch_and_display(display, jpeg):
    try:
        print("Fetching image...")
        width, height = display.get_bounds()
        url = f"{URL}?width={width}&height={height}"
        print(url)
        while True:
            response = urequests.get(url)
            print('here')
            if response.status_code == 200:
                print("Image received, displaying...")
                display_image(display, jpeg, response.content)
            else:
                print("Failed to fetch image:", response.status_code)
            response.close()
            time.sleep(60)  # Wait for 1 minute before fetching again
    except Exception as e:
        print("Error fetching image:", e)


def main():
    connect_wifi()
    display = setup_display()
    jpeg = setup_jpeg(display)
    fetch_and_display(display, jpeg)


main()
