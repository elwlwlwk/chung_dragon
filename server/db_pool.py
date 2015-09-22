from pymongo import MongoClient as Connection
from config import DB_HOST, MONGO_AUTHENTICATE

MongoDB= Connection(DB_HOST, wtimeout=1).dragon
MongoDB.authenticate(MONGO_AUTHENTICATE['id'], MONGO_AUTHENTICATE['passwd'])
