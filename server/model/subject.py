import datetime

from mongoengine import DynamicDocument, DateTimeField, ReferenceField, DynamicField
from .reasearch import Research


class Subject(DynamicDocument):
    meta = {
        'collection': 'subjects'
    }

    info = DynamicField(default={})
    research_id = ReferenceField(Research, required=True, dbref=False)
    created_at = DateTimeField(required=True, default=datetime.datetime.utcnow)
