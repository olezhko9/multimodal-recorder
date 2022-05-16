from mongoengine import StringField, BooleanField, ListField, EmbeddedDocument, \
    EmbeddedDocumentField, DynamicField, DynamicDocument


class DeviceSetting(EmbeddedDocument):
    type = StringField(default='string')
    name = StringField(required=True)
    label = StringField(required=True)
    default = DynamicField()
    options = ListField(StringField())


class Device(DynamicDocument):
    meta = {
        'collection': 'devices'
    }

    device_id = StringField(required=True)
    name = StringField(required=True, max_length=256)
    stream = BooleanField()
    class_name = StringField(required=True, db_field='class')
    settings = ListField(EmbeddedDocumentField(DeviceSetting))
