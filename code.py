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
from adafruit_led_animation.animation.sparkle import Sparkle
import board
import neopixel
from rainbowio import colorwheel
from ulab import numpy as np


# Customize your neopixel configuration here...
pixel_pin = board.IO7
num_pixels = 150
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=neopixel.RGBW
)

# secrets.py has SSID/password and adafruit.io
ADAFRUIT_IO_USERNAME = "mminton"
ADAFRUIT_IO_KEY = "aio_qdPH50d4hiRIXQOorYv89Q5be9l5"

NUMBERPAD = "lulus.numberpad"

wifi.radio.connect("Lulu's Guest", "unicorngiggles")

# Setup Adafruit IO connection
POOL = socketpool.SocketPool(wifi.radio)
REQUESTS = adafruit_requests.Session(POOL, ssl.create_default_context())
# Initialize an Adafruit IO HTTP API object
IO = IO_HTTP(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY, REQUESTS)

RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
YELLOW_ORANGE = (80, 170, 0, 0)
YELLOW2 = (180, 255, 0, 0)
ORANGE = (100, 200, 0, 0)
RED2 = (50, 200, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)

def pickRandomColor():
    CYAN = (0, 255, 255, 0)
    BLUE = (0, 0, 255, 0)
    PURPLE = (180, 0, 255, 0)
    return random.choice([CYAN, BLUE, PURPLE])

ddt = np.array([1.,-2.,1.])
def step(u, um, f, n, dx, dt, c):
    dt2 = dt*dt
    C2 = (c*dt/dx)**2
    deriv = np.convolve(u, ddt)[1:-1] * C2
    up = -um + u * 2 + deriv + f * dt2
    up[0] = 0
    up[n-1] = 0

    return up

def main():
    animation_number = 1
    rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
    
    # for animation 3 - random lightning
    comet = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet2 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet3 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet4 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet5 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet6 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet7 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet8 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet9 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)
    comet10 = Comet(pixels, speed=random.random() * 0.2, color=pickRandomColor(), tail_length=int(random.random() * 30), bounce=False)

    # for sunset animation
    sparkleOrange = Sparkle(pixels, speed=0.15, color=ORANGE, num_sparkles=150)
    sparkleYellow = Sparkle(pixels, speed=0.15, color=YELLOW_ORANGE, num_sparkles=150)
    cometRed1 = Comet(pixels, speed=0.2, color=RED2, tail_length=10, bounce=True)
    cometRed2 = Comet(pixels, speed=0.06, color=RED2, tail_length=5, bounce=True)
    cometYellow = Comet(pixels, speed=0.1, color=YELLOW2, tail_length=4, bounce=False)

    # for wave animation
    # This precomputes the color palette for maximum speed
    # You could change it to compute the color palette of your choice
    w = [colorwheel(i) for i in range(256)]

    # This sets up the initial wave as a smooth gradient
    u = np.zeros(num_pixels)
    um = np.zeros(num_pixels)
    f = np.zeros(num_pixels)

    slope = np.linspace(0, 256, num=num_pixels)
    th = 1

    # the first time is always random (is that a contradiction?)
    r = 0
    # end wave animation vars
    
    while True:
        if time.time() % 30 == 0:
            print('time to update')
            try:
                numberpad = IO.get_feed(NUMBERPAD)
                numberpad_data = IO.receive_data(numberpad["key"])
                animation_number = int(numberpad_data["value"])
                print(animation_number)
            except Exception as error:
                print(error)

        if animation_number == 1:
            # RAINBOW DEBUG ANIMATION
            rainbow_comet.animate()
        elif animation_number == 2:
            # WAVE ANIMATION
            # Some of the time, add a random new wave to the mix
            # increase .15 to add waves more often
            # decrease it to add waves less often
            if r < .01:
                ii = random.randrange(1, num_pixels-1)
                # increase 2 to make bigger waves
                f[ii] = (random.random() - .5) * 2

            # Here's where to change dx, dt, and c
            # try .2, .02, 2 for relaxed
            # try 1., .7, .2 for very busy / almost random
            u, um = step(u, um, f, num_pixels, .1, .02, 1), u

            v = u * 200000 + slope + th
            for i, vi in enumerate(v):
                # Scale up by an empirical value, rotate by th, and look up the color
                pixels[i] = w[round(vi) % 256]

            # Take away a portion of the energy of the waves so they don't get out
            # of control
            u = u * .99

            # incrementing th causes the colorwheel to slowly cycle even if nothing else is happening
            th = (th + .25) % 256
            pixels.show()

            # Clear out the old random value, if any
            f[ii] = 0

            # and get a new random value
            r = random.random()
        elif animation_number == 3:
            # RANDOM LIGHTNING ANIMATION
            random.choice([comet, comet2, comet3, comet4, comet5, comet6, comet7, comet8, comet9, comet10]).animate()
        elif animation_number == 4:
            # AFTERNOON CLOUDS ANIMATION
            sparkleOrange.animate()
            sparkleYellow.animate()
            cometRed1.animate()
            cometRed2.animate()
            cometYellow.animate()
        else:
            pixels.fill(GREEN)
            pixels.show()

main()
