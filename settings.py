import json
import os.path


# set and get methods within domains.
# domain is a json file in 'cfg' subdirectory
# on get lazy loads as needed
# calling set triggers a write

_DATA = {}


def getDataFile(domain):
    return "./cfg/" + domain + ".json"


def set(domain, key, value):
    global _DATA
    if domain not in _DATA:
        _DATA[domain] = {}
    _DATA[domain][key] = value
    with open(getDataFile(domain), "w") as out:
        json.dump(_DATA[domain], out)


def get(domain, key):
    global _DATA
    if domain not in _DATA:
        if os.path.isfile(getDataFile(domain)):
            with open(getDataFile(domain)) as infile:
                _DATA[domain] = json.load(infile)
        else:
            return None
        if key not in _DATA[domain]:
            return None
        return _DATA[domain][key]
