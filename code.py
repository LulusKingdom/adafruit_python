import random
import ssl
import time
import adafruit_requests
import socketpool
import wifi
from adafruit_io.adafruit_io import IO_HTTP
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.comet import Comet
import board
import neopixel
from rainbowio import colorwheel
from ulab import numpy as np


# Customize your neopixel configuration here...
pixel_pin = board.IO7
num_pixels = 15
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=neopixel.RGBW
)

# secrets.py has SSID/password and adafruit.io
ADAFRUIT_IO_USERNAME = "mminton"
ADAFRUIT_IO_KEY = "aio_QMnN75m5hEyVV9RWdpxgf7UN49Kg"

NUMBERPAD = "lulus.numberpad"

wifi.radio.connect("Lulu's Guest", "unicorngiggles")

# Setup Adafruit IO connection
POOL = socketpool.SocketPool(wifi.radio)
REQUESTS = adafruit_requests.Session(POOL, ssl.create_default_context())
# Initialize an Adafruit IO HTTP API object
IO = IO_HTTP(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY, REQUESTS)

RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)


def main():
    animation_number = 1
    rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
    print(rainbow_comet)
    while True:
        if time.time() % 30 == 0:
            try:
                numberpad = IO.get_feed(NUMBERPAD)
                numberpad_data = IO.receive_data(numberpad["key"])
                animation_number = int(numberpad_data["value"])
            except Exception as error:
                print(error)
        print(animation_number)
        if animation_number == 1:
            rainbow_comet.animate()
        elif animation_number == 2:
            pixels.fill(YELLOW)
            pixels.show()
        else:
            pixels.fill(GREEN)
            pixels.show()


main()
