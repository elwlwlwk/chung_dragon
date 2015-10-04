import os
import pika
import uuid
import asyncio
import logging

class RpcSensor(object):
	def __init__(self, sensor_name, config):
		print('Initializing %s sensor' % sensor_name)
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
				host='localhost'))

		self.connection.add_timeout(1, self.on_timeout)
		self.channel = self.connection.channel()

		result = self.channel.queue_declare(exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(self.on_response, no_ack=True,
			queue=self.callback_queue)
		self.name= sensor_name
		self.config= config
		os.system(self.config["script"])
		self.loop = asyncio.get_event_loop()
		self.set()
	
	def on_timeout(self):
		pass
	def set(self):
		self.handler = self.loop.call_later(int(self.config['refresh_interval']), self.run)

	def run(self):
		self.set()
		print("%s : %s %s" % (self.name, self.call().decode(),self.config["unit"]))

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body

	def call(self):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',
			routing_key = self.config["routing_key"],
			properties = pika.BasicProperties(
				reply_to = self.callback_queue,
				correlation_id = self.corr_id,
				),
			body=self.config["rpc_body"])
		while self.response is None:
			self.connection.process_data_events()
		return (self.response)
