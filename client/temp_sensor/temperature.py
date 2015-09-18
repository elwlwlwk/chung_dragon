from sht1x.Sht1x import Sht1x as SHT1x
dataPin=11
clkPin=7 
sht1x= SHT1x(dataPin, clkPin, SHT1x.GPIO_BCM)

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_temperature')

def temperature():
    return sht1x.read_temperature_C()

def humidity():
    return sht1x.read_humidity()

def on_request(ch, method, props, body):
    temp = temperature()

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(temp))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_temperature')

print " [x] Awaiting RPC requests"
channel.start_consuming()
