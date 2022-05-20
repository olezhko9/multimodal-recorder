from bson import ObjectId

from config import config
from model.subject import Subject


def get_subjects(research_id):
    subjects = Subject.objects(research_id=research_id)
    return [subject.to_mongo() for subject in subjects]


def get_subject(subject_id):
    subject = Subject.objects(_id=ObjectId(subject_id)).first()
    if subject:
        return subject.to_mongo()


def create_subject(research_id, subject_data):
    subject = Subject(research_id=research_id, info=subject_data)
    res = subject.save()
    return res.to_mongo()


def delete_subject(subject_id):
    subject = Subject.objects(_id=ObjectId(subject_id)).first()
    if subject:
        subject.delete()


def get_subject_dir(research_id, subject_id):
    data_dir = config.get('data_dir')
    return f'{data_dir}/research_{research_id}/subject_{subject_id}'
