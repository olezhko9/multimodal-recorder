import datetime

from mongoengine import DynamicDocument, DateTimeField, ReferenceField, DictField
from .reasearch import Research
from .subject import Subject


class ResearchRecord(DynamicDocument):
    meta = {
        'collection': 'records'
    }

    research_id = ReferenceField(Research, required=True, dbref=False)
    subject_id = ReferenceField(Subject, required=True, dbref=False)
    device_modality_dict = DictField()
    created_at = DateTimeField(required=True, default=datetime.datetime.utcnow)
