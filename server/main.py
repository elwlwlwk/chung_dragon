from flask import Flask, request
app= Flask(__name__)

@app.route('/')
def root():
    return 'root'
	
@app.route('/sensors', methods=['POST','GET', 'PUT', 'DELETE'])
def sensors():
	return request.method

if __name__=='__main__':
	app.run(host='0.0.0.0', debug= True)


