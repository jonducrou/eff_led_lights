import random
from noise import pnoise2, snoise2

octaves = 1
freq = 16.0 * octaves
POS = random.random()*100


def getDefaultParams():
    return {"colour": (100, 100, 100)}

def customParams():
    return [
        {"name": "colour", "type": "rgb"},
        ]

def assignSafe(grid, x, y, w, h, value):
  if (x < w and x>= 0 and y < h and y>= 0):
    grid[x][y] = value
def capAt255(x):
  return capAt(x,255)
def capAt(x,c):
  if (x>c):
    return c
  return x
def floorAt(x,c):
  if (x<c):
    return c
  return x
def getV():
  r = random.random()
  if(r<0.5):
    r -= 1
  return r


def mapToColour(x, type="gb_line"):
  if (type == "gb_line"):
    if (x < 44):
      return (0,0,0)
    elif (x< 128):
      return (0,int((x-44)*255/(128-44)),0)
    elif (x< 214):
      return (0,0, int(-(x-214)*255/(214-128)))
    else:
      return (0,0,0)


def go(params, h, w, led_control):
    global POS
    POS += 0.001

    r = params["colour"][0]
    g = params["colour"][1]
    b = params["colour"][2]

    for x in range(w):
        for y in range(h):
            #v = capAt(floorAt(int((snoise2(pos+x/freq, pos+y/freq, octaves)*255+64)),0),255)
            v = capAt(floorAt(int((snoise2(POS+x/freq, POS+y/freq, octaves)*127+128)),0),255)
            cm = mapToColour(v,"gb_line")
            led_control.setLEDs(x,y,cm[0],cm[1],cm[2])

