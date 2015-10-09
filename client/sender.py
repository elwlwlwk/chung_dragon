import http.client
import urllib.parse
import json
from time import time

class HttpSender:
	def __init__(self):
		pass
	def post_data(self,url, data):
		self.conn= http.client.HTTPConnection("pi.wisewolf.org:5000")
		header= {"Content-type":"application/json",\
"Accept": "text/plain"}
		self.conn.request("POST",url, data, header)
	
	def send_sensor_value(self, rpi_id, sensor_id, value):
		data= json.dumps({"rpi_id":rpi_id, "sensor_id":sensor_id, "value":value, "time":int(time()*1000)})		
		self.post_data("/data", data)

	def send_rpi_data(self, rpi_id, rpi_cord, sensor_list):
		data= json.dumps({"rpi_id":rpi_id, "cordinate":rpi_cord,"sensor_list":sensor_list})
		self.post_data("/raspberrypi/"+rpi_id, data)
