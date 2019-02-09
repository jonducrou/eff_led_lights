import led_control
import led_configuration
import settings
from vis import gridder
from pystalkd.Beanstalkd import Connection
import numbers
import json

# contains
#  the main loop
#  beanstalk listener
#  vis load and unload
#  ability to go into configure mode


# register beanstalk listener
BS = Connection()

# init the leds
led_control.init()

# other globals
VIS_CURRENT = "gridder"
VIS_LIST = {
    "gridder": gridder
}
VIS_PARAMS = settings.getAll(VIS_CURRENT)
if VIS_PARAMS is None:
    VIS_PARAMS = VIS_LIST[VIS_CURRENT].getDefaultParams()
    settings.create(VIS_CURRENT, VIS_PARAMS)
    lst = settings.get("core", "vis_list")
    if lst is None:
        lst = []
    lst.append(VIS_CURRENT)
    settings.set("core", "vis_list", list(set(lst)))
    settings.set("custom", VIS_CURRENT, VIS_LIST[VIS_CURRENT].customParams())


# change the state based on a connections
def process_event(msg):
    global VIS_CURRENT, VIS_PARAMS
    print(msg)
    if ("action" not in msg):
        print("ERROR: No action")
        return
    if ("params" not in msg):
        print("ERROR: No params")
        return
    action = msg["action"]
    params = msg["params"]
    if ("setDim" == action):
        if (isInstance(params, numbers.Number) and params <= 1 and params > 0):
            settings.set("core", "dim", params)
        else:
            print("ERROR: Can't dim to " + str(params))
    elif("update" == action):
        VIS_CURRENT = params
        settings.loadFromFile(params)
        VIS_PARAMS = settings.getAll(VIS_CURRENT)
    elif("configure" == action):
        led_configuration.run_configuration(led_control)

def main_loop():
    global VIS_CURRENT, VIS_PARAMS
    job = BS.reserve(0)
    if (not job == None):
        job.delete()
        process_event(json.loads(job.body))

    resolution = settings.get("core", "resolution")
    VIS_LIST[VIS_CURRENT].go(VIS_PARAMS, resolution[0], resolution[1], led_control)
    led_control.flush()

while(True):
    main_loop()
