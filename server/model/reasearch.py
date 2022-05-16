import datetime

from mongoengine import StringField, ListField, DynamicDocument, DateTimeField


class Research(DynamicDocument):
    meta = {
        'collection': 'researches'
    }

    name = StringField(required=True, db_field='name')
    description = StringField(required=True)
    devices = ListField()
    created_at = DateTimeField(required=True, default=datetime.datetime.utcnow)
