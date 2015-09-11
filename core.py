import configparser
import json
import pika
import uuid

response=""
corr_id=""
correlation_id=""
sensorList=[]

config= configparser.ConfigParser()
config.read("server.conf")
sensors= json.loads(config['SERVER']['sensors'])

class RpcSensor(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, sensor):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key = sensor['routing_key'],
                                   properties = pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=sensor['rpc_body'])
        while self.response is None:
            self.connection.process_data_events()
        return (self.response)

for sensor in sensors:
	sensor_rpc = RpcSensor()
	response = sensor_rpc.call(config[sensor])
	sensorList.append(sensor_rpc)
	print("Got %r" % (response))
