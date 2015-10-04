import pika
import subprocess

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))

channel = connection.channel()

channel.queue_declare(queue = 'rpc_dust')

def on_request(ch, method, props, body):
	dust = subprocess.Popen(["./dust"], stdout=subprocess.PIPE).stdout.readline().decode("utf-8")
	ch.basic_publish(exchange='', 
					routing_key = props.reply_to, 
					properties = pika.BasicProperties(correlation_id = \
					props.correlation_id), 
					body = str(dust))
	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count = 1)
channel.basic_consume(on_request, queue = 'rpc_dust')

print ("[x] Awaiting RPC requests")
channel.start_consuming()
