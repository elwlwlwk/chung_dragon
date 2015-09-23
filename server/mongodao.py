from db_pool import MongoDB

class MongoDAO:
	def __init__(self, db= MongoDB):
		self.db= db
	def insert_sensor_result(self, sensor, value, time, ID, pos, meta):
		pass
