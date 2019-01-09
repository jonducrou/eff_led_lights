import led_control
import led_configuration
import settings
from vis import gridder
from pystalkd.Beanstalkd import Connection
import numbers

# contains
#  the main loop
#  beanstalk listener
#  vis load and unload
#  ability to go into configure mode


#register beanstalk listener
BS = Connection()

#init the leds
led_control.init()

#other globals
VIS_CURRENT = gridder.go
VIS_PARAMS = {"grid_size": 40}
VIS_LIST = {
    "gridder": gridder.go
}

#change the state based on a connections
def process_event(msg):
    global VIS_CURRENT, VIS_PARAMS
    if (not "action" in msg):
         print("ERROR: No action")
         return
    if (not "params" in msg):
         print("ERROR: No params")
         return
    action = msg["action"]
    params = msg["params"]
    if ("setDim" == action):
        if (isInstance(params, number.Number) and params <= 1 and params > 0):
            settings.set("core","dim",params)
        else:
            print("ERROR: Can't dim to " + str(params))
    elif("setVis" == action):
        VIS_CURRENT = VIS_LIST[action]
        VIS_PARAMS = params

#main_loop
def main_loop():
    global VIS_CURRENT, VIS_PARAMS
    job = BS.reserve(0)
    if (not job == None):
        process_event(json.loads(job.body))
        job.delete()

    resolution = settings.get("core", "resolution")
    VIS_CURRENT(VIS_PARAMS, resolution[0], resolution[1], led_control)
    led_control.flush()

while(True):
    main_loop()
