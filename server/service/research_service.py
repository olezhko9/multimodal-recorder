from model.reasearch import Research
from bson import ObjectId


def get_researches():
    researches = Research.objects()
    return [research.to_mongo() for research in researches]


def create_research(research_data):
    research = Research(**research_data)
    res = research.save()
    return res.to_mongo()


def delete_research(research_id):
    research = Research.objects(_id=ObjectId(research_id)).first()
    if research:
        research.delete()

