import json
import settings
import board
import neopixel
import time
from colorama import Fore, Back, Style
import colorama
colorama.init()

canvas = ()
pixels = []


def init():
    global canvas
    global pixels
    resolution = settings.get('core', 'resolution')
    h = resolution[0]
    w = resolution[1]

    pixels = neopixel.NeoPixel(board.D18, 310, auto_write=False)

    dim = 0.1

    canvas = [[(0, 0, 0) for x in range(h)] for y in range(w)]


# this should be exported to a different module
def mapToColour(x, type="gb_line"):
    if (type == "gb_line"):
        if (x < 44):
            return (0, 0, 0)
        elif (x < 128):
            return (0, int((x-44)*255/(128-44)), 0)
        elif (x < 214):
            return (0, 0, int(-(x-214)*255/(214-128)))
        else:
            return (0, 0, 0)
    elif (type == "star"):
        if (x < 180):
            return (0, 0, 0)
        elif (x < 200):
            v = int((x-180)*255/20)
            return (0, 0, v)
        elif (x < 220):
            v = int(-(x-220)*100/20)
            return (v, v, 255)
        else:
            return (100, 100, 255)


def flush():
    global canvas, pixels
    resolution = settings.get('core', 'resolution')
    h = resolution[0]
    w = resolution[1]

    base_str = 100
    pixels.show()
    print("\n\n\n\n\n\n")
    for x in range(w):
        for y in range(h):
            r = canvas[x][y][0]
            g = canvas[x][y][1]
            b = canvas[x][y][2]
            if (r + b < g and g > 2*base_str):
                print(Back.GREEN + Fore.GREEN + "X", end='')
            elif (r + b < g and g > base_str):
                print(Back.RESET + Fore.GREEN + "X", end='')
            elif (r + g < b and b > 2*base_str):
                print(Back.BLUE + Fore.BLUE + "X", end='')
            elif (r + g < b and b > base_str):
                print(Back.RESET + Fore.BLUE + "X", end='')
            elif (g + b < r and r > base_str):
                print(Back.RESET + Fore.RED + "X", end='')
            elif (r + g + b > 200):
                print(Back.RESET + Fore.WHITE + "X", end='')
            else:
                print(Style.RESET_ALL + " ", end='')
        print(Style.RESET_ALL)
    else:
        print ("!")


def setLED(i, r, g, b):
    dim = settings.get('core', 'dim')
    pixels[i] = (int(r*dim), int(g*dim), int(b*dim))


def setLEDs(x, y, r, g, b):
    global canvas
    grid = settings.get('ledspace', 'grid')
    for i in grid[x][y]:
        setLED(i, r, g, b)
        canvas[x][y] = (r, g, b)


def fill(r, g, b):
    num_pixels = settings.get('core', 'numPixels')
    for i in range(num_pixels):
        setLED(i, r, g, b)
