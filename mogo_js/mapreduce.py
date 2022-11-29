from pymongo import MongoClient
from pymongo.code import Code


connection = MongoClient('localhost', 50002)
db = connection.obama


# db.texts.remove()
with open("../mongo/obama.txt", "r") as f:
    lines = f.readlines()

[db.texts.insert({"text": line}) for line in lines]

with open("wordmap.js", "r") as f:
    map = Code(f.read())


with open("wordreduce.js", "r") as f:
    reduce = Code(f.read())


results = db.texts.map_reduce(map, reduce)

for result in results.find():
    print(result["id"], result["value"]["count"])
