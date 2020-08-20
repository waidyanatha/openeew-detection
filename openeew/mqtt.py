import json
from time_utils import set_time


def parser_json(payload):
    '''
    Parser payload from mqtt
    Format json
    Returns:
        device_id
        cloud_t
        traces
        sr
    where:
    traces =  {"t" : numpy.array(t), "x" : numpy.array(x), "y" : numpy.array(y), "z" : numpy.array(z)}

    '''
    payload = json.loads(payload)
    device_id = payload["device_id"]
    cloud_t = payload["cloud_t"]

    # jsonl from esp32 sensors
    if len(payload) == 3:
        _x = []
        _y = []
        _z = []
        _t = []

        for i, item in enumerate(payload["traces"]):
            _x.append(item["x"])
            _y.append(item["y"])
            _z.append(item["z"])
            _t.append(item["t"])
            sr = item["sr"]

        x = [item for sublist in _x for item in sublist]
        y = [item for sublist in _y for item in sublist]
        z = [item for sublist in _z for item in sublist]

        # Set times per each data tupple (x, y and z)
        t = set_time(_t, sr, len(x))

        traces = {"t": t, "x": x, "y": y, "z": z}

    # jsonl from rp sensors
    elif len(payload) == 8:

        sr = payload["sr"]
        x = payload["x"]
        y = payload["y"]
        z = payload["z"]
        _t = [payload["device_t"]]
        t = set_time(_t, sr, len(x))

        traces = {"t": t, "x": x, "y": y, "z": z}

    return device_id, cloud_t, traces, sr
