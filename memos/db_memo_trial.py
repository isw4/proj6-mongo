"""
Adding some default values into the db in order to test if the template would
display the contents properly. There should be at least 3 notes displayed after 
this is run. This script WILL REMOVE OLD MEMO
S"""

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import arrow
import sys

import config
CONFIG = config.configuration()

MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST, 
    CONFIG.DB_PORT, 
    CONFIG.DB)

print("Using URL '{}'".format(MONGO_CLIENT_URL))

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    print("Attempting database: {}".format(CONFIG.DB))
    collection = getattr(db, CONFIG.DB_COLLECTION)
    print("Attempting collection: {}".format(CONFIG.DB_COLLECTION))
except Exception as err:
    print("Failed")
    print(err)
    sys.exit(1)


#
# Insertions
# 
print("\nDeleting old entries")
collection.delete_many({})

print("\nCreating index")
collection.create_index("score")

lorem = "Spicy jalapeno bacon ipsum dolor amet tri-tip qui pork loin, magna meatloaf pastrami in. Velit labore ham hock, occaecat sirloin meatball culpa beef ribs cillum kielbasa id shoulder rump adipisicing. Picanha dolor exercitation, flank swine adipisicing beef ribs pork chop filet mignon eiusmod veniam. Frankfurter strip steak eu, tongue bacon jerky elit duis id leberkas eiusmod kielbasa tail adipisicing."

print("\nInserting memos")
timenow = arrow.utcnow();
mem = { 
        "type": "dated_memo",
        "date":  timenow.isoformat(),
        "score": timenow.isoformat().split('T')[0].replace('-', ''),
        "text": "This is the first inserted memo. "+lorem
      }

print("Inserting 1st memo")
collection.insert(mem)
print("Inserted")

first = collection.find_one()
first_id = str(first['_id'])
print("The id as a string of the first memo is {}".format(first_id))

timenow = arrow.utcnow();
mem = { 
        "type": "dated_memo",
        "date":  timenow.isoformat(),
        "score": timenow.isoformat().split('T')[0].replace('-', ''),
        "text": "This is the second inserted memo. "+lorem
      }

print("Inserting 2nd memo")
collection.insert(mem)
print("Inserted")

timenow = arrow.utcnow();
mem = { 
        "type": "dated_memo",
        "date":  timenow.isoformat(),
        "score": timenow.isoformat().split('T')[0].replace('-', ''),
        "text": "This is the third inserted memo. "+lorem
      }

print("Inserting 3rd memo")
collection.insert(mem)
print("Inserted")

timenow = arrow.utcnow().shift(days=-2);
mem = { 
        "type": "dated_memo",
        "date":  timenow.isoformat(),
        "score": timenow.isoformat().split('T')[0].replace('-', ''),
        "text": "This is the fourth inserted but temporally earliest memo. "+lorem
      }

print("Inserting 4th memo")
collection.insert(mem)
print("Inserted")


#
# Looking up by id
#
found = collection.find_one({'_id': ObjectId(first_id)})
found_text = found['text']
print("\nThe text of the first inserted memo is: {}".format(found_text))


#
# Deleting by id. Commented out if just want to populate db with default items
#
# res = collection.delete_one({'_id': ObjectId(first_id)})
# print("Deleted {} number of entries".format(res.deleted_count))


#
# Sorting by score
#
print("\nListing memos by score")
for memo in collection.find().sort('score', pymongo.ASCENDING):
    print(memo['text'])