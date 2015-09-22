from flask import Flask, request
from db_pool import MongoDB
app= Flask(__name__)

@app.route('/')
def root():
    return 'root'
	
@app.route('/sensors', methods=['POST','GET', 'PUT', 'DELETE'])
def sensors():
	if request.method == 'GET':
		MongoDB.sensor_value.insert({"test2":"test2"})
	return request.method

if __name__=='__main__':
	app.run(host='0.0.0.0', debug= True)
