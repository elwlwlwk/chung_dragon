import configparser
import json
import uuid
from rpcsensor import RpcSensor

response=""
corr_id=""
correlation_id=""
sensorList=[]

config= configparser.ConfigParser()
config.read("server.conf")
sensors= json.loads(config['SERVER']['sensors'])

for sensor in sensors:
	sensorList.append(RpcSensor(sensor, config[sensor]))
