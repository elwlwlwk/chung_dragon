from flask import Flask, request
from db_pool import MongoDB
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(HelloWorld, "/")

# from 위치:string, ID:string, 센서값:string, 센서 종류:string, 단위:string

SENSERS = {}

class Sensors(Resource):
    def get(self):
        return SENSERS
    def put(self):
        pass

api.add_resource(Sensors, "/sensors")

class Sensor(Resource):
    def get(self, sensor_id):
        return SENSERS[sensor_id]
    def post(self, sensor_id):
        pass
    def put(self, sensor_id):
        pass
    def delet(self, sensor_id):
        pass

api.add_resource(Sensor, "/sensors/<string:sensor_id>")

if __name__=='__main__':
    app.run(host='0.0.0.0', debug= True)
