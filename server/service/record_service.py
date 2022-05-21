from bson import ObjectId

from config import config
from model.research_record import ResearchRecord


def get_records(research_id, subject_id):
    records = ResearchRecord.objects(research_id=research_id, subject_id=subject_id)
    return [record.to_mongo() for record in records]


def get_record(record_id):
    record = ResearchRecord.objects(_id=ObjectId(record_id)).first()
    if record:
        return record.to_mongo()


def create_record(research_id, subject_id):
    record = ResearchRecord(research_id=research_id, subject_id=subject_id)
    res = record.save()
    return res.to_mongo()


def delete_record(record_id):
    record = ResearchRecord.objects(_id=ObjectId(record_id)).first()
    if record:
        record.delete()


def get_record_dir(record_id):
    data_dir = config.get('data_dir')
    record = get_record(record_id)
    if record:
        return f"{data_dir}/research_{record['research_id']}/subject_{record['subject_id']}/records/record_{record_id}"
