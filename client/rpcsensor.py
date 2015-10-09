import os
import pika
import uuid
import asyncio
import logging
import time

from sender import HttpSender

class RpcSensor(object):
	def __init__(self, rpi_id, sensor_name, config):
		print('Initializing %s sensor' % sensor_name)
		self.sender= HttpSender()
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
				host='localhost'))

		self.channel = self.connection.channel()

		result = self.channel.queue_declare(exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(self.on_response, no_ack=True,
			queue=self.callback_queue)
		self.rpi_id= rpi_id
		self.name= sensor_name
		self.config= config
		os.system(self.config["script"])
		self.loop = asyncio.get_event_loop()
		self.timeout= 1
		self.set()
	
	def set(self):
		self.handler = self.loop.call_later(int(self.config['refresh_interval']), self.run)

	def run(self):
		self.set()
		value= self.call().decode()
		print("%s : %s %s" % (self.name, value,self.config["unit"]))
		self.sender.send_sensor_value(self.rpi_id, self.name, value)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	def call(self):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		old_time= time.time()
		self.channel.basic_publish(exchange='',
			routing_key = self.config["routing_key"],
			properties = pika.BasicProperties(
				reply_to = self.callback_queue,
				correlation_id = self.corr_id,
				),
			body=self.config["rpc_body"])
		while self.response is None:
			if time.time()- old_time > self.timeout:
				return b""
			self.connection.process_data_events()
		return (self.response)
