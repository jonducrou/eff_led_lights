import json
import board
import neopixel
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep


NUM_PIXELS = 310
locations = []
RESOLUTION = (64,48)

data = [None for i in range(NUM_PIXELS)]

pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS)

def collect(i, img0, imgR, imgG, imgB):
  x = None
  y = None
  biggestR = 0
  locR = (0,0)
  biggestG = 0
  locG = (0,0)
  biggestB = 0
  locB = (0,0)
  for y in range(RESOLUTION[0]):
    for x in range(RESOLUTION[1]):
      if (imgR[x,y,1] < img0[x,y,1]):
        rVal = 0
      else:
        rVal = imgR[x,y,1] - img0[x,y,1]
      if (rVal > biggestR):
        biggestR = rVal
        locR = (x,y)

      if (imgG[x,y,1] < img0[x,y,1]):
        gVal = 0
      else:
        gVal = imgG[x,y,1] - img0[x,y,1]
      if (gVal > biggestG):
        biggestG = gVal
        locG = (x,y)

      if (imgB[x,y,1] < img0[x,y,1]):
        bVal = 0
      else:
        bVal = imgB[x,y,1] - img0[x,y,1]
      if (bVal > biggestB):
        biggestB = bVal
        locB = (x,y)

  print("R: " + str(biggestR))
  print (locR)
  print("G: " + str(biggestG))
  print (locG)
  print("B: " + str(biggestB))
  print (locB)

  print()
  data[i] = [locR, locG, locB]
  return (x,y)

with PiCamera() as camera:
 camera.resolution = RESOLUTION
 with PiRGBArray(camera, size=RESOLUTION) as output:
  # for each pixel
  for i in range(NUM_PIXELS):
    if (i<20):
      continue
    # read from camera -> img 1
    camera.capture(output, 'rgb')
    #camera.capture(str(i) + "-0.jpg")
    img0 = output.array
    output.truncate(0)
    # set pixel red
    pixels[i] = (255,0,0)
    # read from camera -> img 2
    camera.capture(output, 'rgb')
    #camera.capture(str(i) + "-r.jpg")
    imgR = output.array
    output.truncate(0)
    # set pixel green
    pixels[i] = (0,255,0)
    # read from camera -> img 3
    camera.capture(output, 'rgb')
    imgG = output.array
    output.truncate(0)
    # set pixel blue
    pixels[i] = (0,0,255)
    # read from camera -> imgB
    camera.capture(output, 'rgb')
    imgB = output.array
    output.truncate(0)
    # set pixel black
    pixels[i] = (0,0,0)
    # compare images
    collect(i, img0, imgR, imgG, imgB)


    locs = [(0,0) for i in range(NUM_PIXELS)]
    grid = [[0 for i in range(RESOLUTION[0])] for j in range(RESOLUTION[1])]
    gridDetailed = [ [ [] for i in range(RESOLUTION[0] ) ] for j in range(RESOLUTION[1])]

    for i in range(NUM_PIXELS):
     if (data[i] != None):
      #if two of the three agree... good enough for me.
      rx = data[i][0][0]
      ry = data[i][0][1]
      gx = data[i][1][0]
      gy = data[i][1][1]
      bx = data[i][2][0]
      by = data[i][2][1]

      if (rx == gx and ry == gy):
       locs[i] == (gx,gy)
       grid[gx][gy] += 1
       gridDetailed[gx][gy].append(i)
      elif (rx == bx and ry == by):
       locs[i] == (rx,ry)
       grid[rx][ry] += 1
       gridDetailed[rx][ry].append(i)
      elif (gx == bx and gy == by):
       locs[i] == (gx,gy)
       grid[gx][gy] += 1
       gridDetailed[gx][gy].append(i)

    for x in range(RESOLUTION[1]):
      for y in range(RESOLUTION[0]):
       if(grid[x][y]>0):
        print(grid[x][y], end='')
       else:
        print(" ",end='')
      print()

    with open('grid.json', 'w') as out:
      json.dump(gridDetailed, out)
