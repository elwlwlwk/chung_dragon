import logging
import configparser
import json
import uuid
import asyncio
from rpcsensor import RpcSensor
from sender import HttpSender

response=""
corr_id=""
correlation_id=""
sensorList=[]

config= configparser.ConfigParser()
config.read("config.conf")
sensors= json.loads(config['SERVER']['sensors'])
rpi_id= config['SERVER']['id']
cord= json.loads(config['SERVER']['cordinate'])

sender= HttpSender()
sensor_data=[]
for sensor in sensors:
	sensorList.append(RpcSensor(rpi_id, sensor, config[sensor]))
	sensor_data.append({"sensor_id": sensor, "type": config[sensor]['sensor_type'], "unit": config[sensor]["unit"]})

sender.send_rpi_data(rpi_id, cord, sensor_data)
for sensor in sensorList:
	sensor.loop.run_forever()
