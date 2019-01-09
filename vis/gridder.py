


POS=0

def go(params, h, w, led_control):
    global POS
    POS = POS+1
    grid_size = params["grid_size"]
    for x in range(w):
        for y in range(h):
            led_control.setLEDs(x,y,0,0,0)
            if ((POS+x) % grid_size == 0):
                led_control.setLEDs(x,y,100,100,100)
            if ((POS+y) % grid_size == 0):
                led_control.setLEDs(x,y,100,100,100)

            if ((POS+x) % grid_size == 1 or (POS+x) % grid_size == grid_size - 1):
                led_control.setLEDs(x,y,30,0,30)
            if ((POS+y) % grid_size == 1 or (POS+y) % grid_size == grid_size - 1):
                led_control.setLEDs(x,y,30,30,0)
