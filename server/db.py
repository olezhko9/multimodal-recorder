import json

from flask_pymongo import PyMongo
from bson.json_util import ObjectId


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MongoJsonEncoder, self).default(obj)


class DbManager:
    def __init__(self, app):
        self.mongo = PyMongo(app)

    def get_db(self):
        return self.mongo.db
