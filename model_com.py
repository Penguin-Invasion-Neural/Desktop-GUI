from statistics import mean
import requests

def model_com(url, sensor_0, sensor_1, sensor_2, sensor_3):
    req = []
    req.append(100)
    req.append(100)
    req.append(100)

    req.append(mean(sensor_0))
    req.append(max(sensor_0))
    req.append(min(sensor_0))

    req.append(mean(sensor_1))
    req.append(max(sensor_1))
    req.append(min(sensor_1))

    req.append(mean(sensor_2))
    req.append(max(sensor_2))
    req.append(min(sensor_2))

    req.append(mean(sensor_3))
    req.append(max(sensor_3))
    req.append(min(sensor_3))

    body = {'data': req}

    res = requests.post(url, json = body)

    return res
