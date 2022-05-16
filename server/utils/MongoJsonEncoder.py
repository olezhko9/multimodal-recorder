import json

from bson import ObjectId
from datetime import date, datetime

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        return super(MongoJsonEncoder, self).default(obj)
