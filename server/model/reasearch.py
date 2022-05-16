from mongoengine import StringField, ListField, DynamicDocument


class Research(DynamicDocument):
    meta = {
        'collection': 'researches'
    }

    name = StringField(required=True, db_field='name')
    description = StringField(required=True)
    devices = ListField()
