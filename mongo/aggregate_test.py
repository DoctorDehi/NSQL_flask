from pymongo import MongoClient


connection = MongoClient('localhost', 50002)
db = connection.obama

# with open("../mongo/obama.txt", "r") as f:
#     lines = f.readlines()
#
# [db.texts.insert_one({"text": line}) for line in lines]

# for i in db.texts.find({}):
#     print(i)

pipeline = [
    {"$unwind": "$text"},
    {"$count": {"$sum": 1}},
]

db.command('aggregate', 'things', pipeline=pipeline, explain=True)
