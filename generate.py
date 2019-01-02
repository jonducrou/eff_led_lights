import random
from noise import pnoise2, snoise2
import board
import neopixel
import json
from colorama import Fore, Back, Style, init
init()


pixels = neopixel.NeoPixel(board.D18, 310, auto_write=False)

 

h = 64
w = 48

octaves = 1
freq = 16.0 * octaves
dim = 0.1

#read in the mapping file

canvas = [ [ (0,0,0) for x in range(h)] for y in range(w) ]

with open('good-grid.json') as f:
  grid = json.load(f)

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


def flush():
  base_str = 100
  pixels.show()
  #if (False):
  if (True):
   print("\n\n\n\n\n\n")
   for x in range(w):
    for y in range(h):
      r = canvas[x][y][0]
      g = canvas[x][y][1]
      b = canvas[x][y][2]
      #if (0 == len(grid[x][y])):
      #  print(Style.RESET_ALL + " ", end='')
      if (r + b < g and g > 2*base_str):
        print(Back.GREEN + Fore.GREEN + "X",end='')
      elif (r + b < g and g > base_str):
        print(Back.RESET + Fore.GREEN + "X",end='')
      elif (r + g < b and b > base_str):
        print(Back.RESET + Fore.BLUE + "X",end='')
      elif (g + b < r and r > base_str):
        print(Back.RESET + Fore.RED + "X",end='')
      elif (r + g + b > 200):
        print(Back.RESET + Fore.WHITE + "X",end='')
      else:
        print(Style.RESET_ALL + " ", end='')
    print(Style.RESET_ALL);
  else:
    print ("!")

def setLED(i,r,g,b):
  pixels[i] = (int(r*dim),int(g*dim),int(b*dim))
  

def setLEDs(x,y,r,g,b):
  for i in grid[x][y]:
    setLED(i,r,g,b)
  canvas[x][y] = (r,g,b)

def noise():
 pos = random.random()*100
 while (True):
  pos +=0.1
  for x in range(w):
    for y in range(h):
     #if (0 < len(grid[x][y])):  #uncomment for minor speed bonus
      #v = capAt(floorAt(int((snoise2(pos+x/freq, pos+y/freq, octaves)*255+64)),0),255)
      v = capAt(floorAt(int((snoise2(pos+x/freq, pos+y/freq, octaves)*127+128)),0),255)
      cm = mapToColour(v,"gb_line")
      setLEDs(x,y,cm[0],cm[1],cm[2])
      #print(v)
  flush()

GRID_SIZE=40
def gridder():
 pos = 0
 while (True):
  pos = pos+1
  for x in range(w):
    for y in range(h):
      setLEDs(x,y,0,0,0)
      if ((pos+x) % GRID_SIZE == 0):
        setLEDs(x,y,100,100,100)
      if ((pos+y) % GRID_SIZE == 0):
        setLEDs(x,y,100,100,100)

      if ((pos+x) % GRID_SIZE == 1 or (pos+x) % GRID_SIZE == GRID_SIZE - 1):
        setLEDs(x,y,30,30,30)
      if ((pos+y) % GRID_SIZE == 1 or (pos+y) % GRID_SIZE == GRID_SIZE - 1):
        setLEDs(x,y,30,30,30)
  flush()


def fill():
  pos = 0
  while (True):
    pos+=1
    if (pos % 2 == 1):
      pixels.fill((0,10,10))
    else:
      pixels.fill((0,0,0))
  flush()

def assignSafe(grid, x, y, value):
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
def starfall():
 stars = [(w/2,h/2,1,1),(w/2,h/2,-0.1,1),(w/2,h/2,1,-1),(w/2,h/2,-1,-1)]
 sky = [ [ 0 for x in range(h)] for y in range(w) ]
 while (True):
  sky = [ [ int(x*0.9) for x in y] for y in sky ] 
  for i, star in enumerate(stars):
    if (star[0] >= w or star[0] < 0 or star[1] >= h or star[1] < 0):
      stars[i] = (w/2,h/2,getV(), getV())
    star = stars[i]
    assignSafe(sky, int(star[0]), int(star[1]), capAt255(200+sky[int(star[0])][int(star[1])]))
    [ assignSafe(sky, int(star[0]+x), int(star[1]+y), capAt255(100+ sky[capAt(floorAt(int(star[0]+x),0),h-1)][capAt(floorAt(int(star[1]+y),0),w-1)])  ) for x in [-1,1] for y in [-1,1] ]

    stars[i] = (star[0] + star[2], star[1] + star[3], star[2], star[3])
  for x in range(w):
    for y in range(h):
      setLEDs(x,y,int(sky[x][y]/2),sky[x][y],int(sky[x][y]/2))
  flush()

noise()
#gridder()
#fill()
#starfall()
