import datetime

from mongoengine import StringField, DynamicDocument, DateTimeField, ReferenceField
from .reasearch import Research


class ResearchRecord(DynamicDocument):
    meta = {
        'collection': 'records'
    }

    research_id = ReferenceField(Research, required=True, dbref=False)
    directory = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.datetime.utcnow)
