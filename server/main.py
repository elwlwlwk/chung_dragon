from flask import Flask, request, render_template, url_for
from db_pool import MongoDB
from flask_restful import Resource, Api
from bson.json_util import dumps, loads

import json
import datetime

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(HelloWorld, "/")

# Map.html
@app.route('/map/')
def map():
    return render_template('./map.html')


# from 위치:string, ID:string, 센서값:string, 센서 종류:string, 단위:string
db = MongoDB
rpis = db.rpi_info
datas = db.datas

class RaspberryPis(Resource):
    def get(self):
        rpi_list=[]
        for rpi in rpis.find(projection={"_id":False}):
            rpi_list.append(rpi)
        return rpi_list
    
api.add_resource(RaspberryPis, "/raspberrypis")

class RaspberryPi(Resource):
    def get(self,rpi_id):
        return rpis.find_one({"rpi_id": rpi_id}, projection={"_id":False})
    def post(self, rpi_id):
        data= json.loads(request.data.decode("utf-8"))
        if rpis.find_one({"rpi_id":data["rpi_id"]}):
            return {"status":"Duplicated rpi_id"}
        rpis.insert(data)
        return {"status":"OK"}
    def put(self,rpi_id):
        return {"status":"OK"}
    def delete(self,rpi_id):
        rpis.remove({"rpi_id":rpi_id})
    
api.add_resource(RaspberryPi, "/raspberrypi/<string:rpi_id>")

class Data(Resource):
    def get(self,input_json):
        input_json=json.loads(input_json)
        rpi_id=input_json['rpi_id']
        output=[]
        index=0
        for rpi in rpis.find({"rpi_id": rpi_id}):
            _rpi=loads(dumps(rpi))
            for sensor in _rpi["sensor_list"]:
                tmp_sensor={}
                tmp_sensor["type"]=sensor["type"]
                recent_data=datas.find({"sensor_id":sensor["sensor_id"],"rpi_id":rpi_id}).sort("time",-1).limit(1)
                _data=loads(dumps(recent_data))
                tmp_sensor["value"]=_data[0]["value"]
                tmp_sensor["time"]=_data[0]["time"]
                output.append(tmp_sensor)
        print(output)
        return output
            
                
    def post(self,input_json):
        datas.insert(json.loads(request.data.decode('utf-8')))
    def put(self):
        pass
    def delete(self):
        input_json=json.loads(request.data.decode('utf-8'))
        time=input_json['time']
        datas.remove({"time":time})

api.add_resource(Data, "/data/<string:input_json>")

class Sensors(Resource):
    def get(self,sensor_id):
        #return {sensor_id: SENSERS[sensor_id]}
        return '1'
    def put(self):
        pass

api.add_resource(Sensors, "/sensors")

class Sensor(Resource):
    def get(self, sensor_id):
        input_data = json.loads(sensor_id)
        output = input_data['rpi_id']
        return output
    def post(self, sensor_id):
        pass
    def put(self, sensor_id):
        pass
    def delet(self, sensor_id):
        pass

api.add_resource(Sensor, "/sensors/<string:sensor_id>")

if __name__=='__main__':
    app.run(host='0.0.0.0', debug= True)
