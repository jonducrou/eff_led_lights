import random

SKY = []
STARS = []


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




def go(params, h, w, led_control):
    global SKY, STARS
    if len(SKY) == 0:
        SKY = [ [ 0 for x in range(h)] for y in range(w) ]
        STARS = [(w/2,h/2,1,1),(w/2,h/2,-0.1,1),(w/2,h/2,1,-1),(w/2,h/2,-1,-1)]

    r = params["colour"][0]
    g = params["colour"][1]
    b = params["colour"][2]

    SKY = [ [ int(x*0.9) for x in y] for y in SKY ]
    for i, star in enumerate(STARS):
        if (star[0] >= w or star[0] < 0 or star[1] >= h or star[1] < 0):
            STARS[i] = (w/2,h/2,getV(), getV())
            star = STARS[i]
        assignSafe(SKY, int(star[0]), int(star[1]), w, h, capAt255(200+SKY[int(star[0])][int(star[1])]))
        [ assignSafe(SKY, int(star[0]+x), int(star[1]+y), w, h, capAt255(100+ SKY[capAt(floorAt(int(star[0]+x),0),w-1)][capAt(floorAt(int(star[1]+y),0),h-1)])  ) for x in [-1,1] for y in [-1,1] ]

        STARS[i] = (star[0] + star[2], star[1] + star[3], star[2], star[3])
    for x in range(w):
         for y in range(h):
             led_control.setLEDs(x,y,int(r*SKY[x][y]/255),int(g*SKY[x][y]/255),int(b*SKY[x][y]/255))


