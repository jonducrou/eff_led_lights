from picamera import PiCamera
from picamera.array import PiRGBArray
import settings


def run_configuration(led_control):
    NUM_PIXELS = settings.get('core', 'numPixels')
    locations = []
    data = [None for i in range(NUM_PIXELS)]
    RESOLUTION = settings.get('core', 'resolution')
    led_control.fill(0, 0, 0)
    led_control.flush()
    with PiCamera() as camera:
        camera.resolution = RESOLUTION
        with PiRGBArray(camera, size=RESOLUTION) as output:
            # for each pixel
            for i in range(NUM_PIXELS):
                print(i)
                camera.capture(output, 'rgb')
                img0 = output.array
                output.truncate(0)

                led_control.setLED(i, 255, 0, 0)
                led_control.flush()
                camera.capture(output, 'rgb')
                imgR = output.array
                output.truncate(0)

                led_control.setLED(i, 0, 255, 0)
                led_control.flush()
                camera.capture(output, 'rgb')
                imgG = output.array
                output.truncate(0)

                led_control.setLED(i, 0, 0, 255)
                led_control.flush()
                camera.capture(output, 'rgb')
                imgB = output.array
                output.truncate(0)

                led_control.setLED(i, 0, 0, 0)
                led_control.flush()

                x = None
                y = None
                biggestR = 0
                locR = (0, 0)
                biggestG = 0
                locG = (0, 0)
                biggestB = 0
                locB = (0, 0)
                for y in range(RESOLUTION[0]):
                    for x in range(RESOLUTION[1]):
                        if (imgR[x, y, 1] < img0[x, y, 1]):
                            rVal = 0
                        else:
                            rVal = imgR[x, y, 1] - img0[x, y, 1]
                            if (rVal > biggestR):
                                biggestR = rVal
                                locR = (x, y)

                        if (imgG[x, y, 2] < img0[x, y, 2]):
                            gVal = 0
                        else:
                            gVal = imgG[x, y, 2] - img0[x, y, 2]
                            if (gVal > biggestG):
                                biggestG = gVal
                                locG = (x, y)

                        if (imgB[x, y, 0] < img0[x, y, 0]):
                            bVal = 0
                        else:
                            bVal = imgB[x, y, 0] - img0[x, y, 0]
                            if (bVal > biggestB):
                                biggestB = bVal
                                locB = (x, y)
                data[i] = [locR, locG, locB]

    locs = [(0, 0) for i in range(NUM_PIXELS)]
    grid = [[0 for i in range(RESOLUTION[0])] for j in range(RESOLUTION[1])]
    gridDetailed = [[[] for i in range(RESOLUTION[0])] for j in range(RESOLUTION[1])]

    for i in range(NUM_PIXELS):
        if (data[i] is not None):
            rx = data[i][0][0]
            ry = data[i][0][1]
            gx = data[i][1][0]
            gy = data[i][1][1]
            bx = data[i][2][0]
            by = data[i][2][1]

            if (rx == gx and ry == gy):
                locs[i] == (gx, gy)
                grid[gx][gy] += 1
                gridDetailed[gx][gy].append(i)
                continue
            elif (rx == bx and ry == by):
                locs[i] == (rx, ry)
                grid[rx][ry] += 1
                gridDetailed[rx][ry].append(i)
                continue
            elif (gx == bx and gy == by):
                locs[i] == (gx, gy)
                grid[gx][gy] += 1
                gridDetailed[gx][gy].append(i)
                continue
            # ok, if there is a tight average... i guess its ok
            ax = (rx+bx+gx)/3
            ay = (ry+gy+by)/3
            error = abs(ax-rx)+abs(ax-gx)+abs(ax-bx)+abs(ay-ry)+abs(ay-gy)+abs(ay-by)
            if (error < 6):
                locs[i] == (int(ax), int(ay))
                grid[int(ax)][int(ay)] += 1
                gridDetailed[int(ax)][int(ay)].append(i)
                continue
    settings.set('ledspace', 'grid', gridDetailed)
