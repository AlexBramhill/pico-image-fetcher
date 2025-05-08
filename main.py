import network
from picographics import PEN_1BIT, PicoGraphics, DISPLAY_INKY_PACK
import pngdec
import time
import urequests
import utime

# import scheduler
from image_client import ImageClient
from image_renderer.png_renderer import Png_Renderer
from secrets import URL
from wifi_manager import WiFiManager, connect_wifi
from src.cron_scheduler import CronScheduler
from display_controller_factory import DisplayConfig, DisplayController, DisplayControllerFactory


# def fetch_and_display_job(display, pngdecInstance):
#     while True:
#         now = time.localtime()
#         print("Time: {}:{}:{}".format(now[3], now[4], now[5]))
#         if time.time() % 60 != 0:
#             print("Waiting for the right time...")
#             time.sleep(1)
#             continue
#         print("right time {}:{}:{}".format(now[3], now[4], now[5]))
#         fetch_and_display_image(display, pngdecInstance)
#         print("Updated, Waiting for the right time...")
#         time.sleep(1)


# def fetch_and_display_image(display, pngdecInstance):
#     width, height = display.get_bounds()
#     url = f"{URL}?width={width}&height={height}&format=png"

#     print("Fetching image...")
#     print(url)
#     try:
#         response = urequests.get(url)
#         date_header = response.headers.get("Date", None)
#         if date_header:
#             print("Date from header:", date_header)
#             try:
#             parsed_date = time.strptime(
#                 date_header, "%a, %d %b %Y %H:%M:%S %Z")
#             print("Parsed date:", parsed_date)
#             except Exception as e:
#             print("Error parsing date:", e)
#         print(f"{response}")
#     except Exception as e:
#         print("Error fetching image:", e)
#         return
#     print("Response code:", response.status_code)
#     if response.status_code == 200:
#         print("Image received, displaying...")
#         display_png(display, pngdecInstance, response.content)
#     else:
#         print("Failed to fetch image:", response.status_code)
#     response.close()


# def display_png_from_file(display, pngdecInstance, path):
#     with open(path, "rb") as f:
#         pngdecInstance.open_RAM(f.read())
#         pngdecInstance.decode(0, 0)
#     display.update()


# def display_png(display, pngdecInstance, image_bytes):
#     pngdecInstance.open_RAM(image_bytes)
#     pngdecInstance.decode(0, 0)
#     display.update()


def main():
    # display = display_factory.init()
    # pngdecInstance = pngdec.PNG(display)
    # wifi_service.connect_wifi()
    # initial load
    # fetch_and_display_image(display, pngdecInstance)

    # fetch_and_display_job(display, pngdecInstance)
    # config = display.DisplayConfig(
    #     display=DISPLAY_INKY_PACK, pen_type=PEN_1BIT)

    # display_instance = display.Display.get_instance(config)
    INKY_CONFIG = DisplayConfig(display=DISPLAY_INKY_PACK, pen_type=PEN_1BIT)

    displayController = DisplayControllerFactory.get_instance(
        INKY_CONFIG, Png_Renderer)
    wifi_service = WiFiManager()
    scheduler = CronScheduler()
    image_client = ImageClient()
    
    wifi_service.connect()

    scheduler.add_schedule(
        lambda: print("Job 1 executed at", time.localtime()), "*/1 * * * * *"
    ).add_schedule(
        lambda: print("Job 2 executed at", time.localtime()), "*/2 * * * * *"
    ).add_schedule(
        lambda: print("Job 3 executed at", time.localtime()), "*/3 * * * * *"
    ).run_scheduler()

    main()
