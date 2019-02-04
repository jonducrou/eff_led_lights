POS = 0


def getDefaultParams():
    return {"grid_size": 40, "colour": (100, 100, 100)}


def customParams():
    return [
        {"name": "grid_size", "type": "number"},
        {"name": "colour", "type": "rgb"},
        ]


def go(params, h, w, led_control):
    global POS
    POS = POS+1
    grid_size = params["grid_size"]
    r = params["colour"][0]
    g = params["colour"][1]
    b = params["colour"][2]

    for x in range(w):
        for y in range(h):
            led_control.setLEDs(x, y, 0, 0, 0)
            if ((POS+x) % grid_size == 0):
                led_control.setLEDs(x, y, r, g, b)
            if ((POS+y) % grid_size == 0):
                led_control.setLEDs(x, y, r, g, b)

            if ((POS+x) % grid_size == 1 or (POS+x) % grid_size == grid_size - 1):
                led_control.setLEDs(x, y, r/3, g/3, b/3)
            if ((POS+y) % grid_size == 1 or (POS+y) % grid_size == grid_size - 1):
                led_control.setLEDs(x, y, r/3, g/3, b/3)
