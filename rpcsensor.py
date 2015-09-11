import pika
import uuid

class RpcSensor(object):
	def __init__(self, sensor_name, config):
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(
				host='localhost'))

		self.channel = self.connection.channel()

		result = self.channel.queue_declare(exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(self.on_response, no_ack=True,
			queue=self.callback_queue)
		self.name= sensor_name
		self.config= config

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
