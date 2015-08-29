import configparser
import json
import pika
import uuid

response=""
corr_id=""
correlation_id=""

config= configparser.ConfigParser()
config.read("server.conf")
sensors= json.loads(config['SERVER']['sensors'])

def on_response(ch, method, props, body):
	if corr_id == correlation_id:
		response = body

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
result = channel.queue_declare(exclusive=True)
callback_queue = result.method.queue
channel.basic_consume(on_response, no_ack=True, queue=callback_queue)

def call():
	response = None
	corr_id = str(uuid.uuid4())
	channel.basic_publish(exchange='', routing_key='rpc_temperature',\
properties=pika.BasicProperties(reply_to = callback_queue, correlation_id = corr_id,),\
body=str(""))
	while response is None:
		connection.process_data_events()
	print(response)
	return response

print(" [x] Requesting temperature")
response = call()
print(" [.] Got %r" % (response,))
