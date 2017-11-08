"""
Testing the functiosn of the MemoNav class in memo_func.py
"""

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import arrow
import sys

import config
from memo_func import MemoNav

#
# Setting up the collection for testing
#
CONFIG = config.configuration()

MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST, 
    CONFIG.DB_PORT, 
    CONFIG.DB)

# Uses a default collection for testing
CONFIG.DB_COLLECTION = "test"

print("Using URL '{}'".format(MONGO_CLIENT_URL))

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    print("Attempting database: {}".format(CONFIG.DB))
    collection = getattr(db, CONFIG.DB_COLLECTION)
    print("Attempting collection: {}".format(CONFIG.DB_COLLECTION))
    db_nav = MemoNav(collection)
except Exception as err:
    print("Setting up test database failed")
    print(err)
    sys.exit(1)

#
# Testing the functions in the MemoNav class. The sequence between tests should be maintained
#
print("\nDeleting old entries")
collection.delete_many({})

def test_insert_one():
	timenow = arrow.utcnow();
	db_nav.insert_one(timenow.isoformat(), "This is the first inserted memo.")
	assert collection.find_one({ 'date': timenow.isoformat() })['text'] == "This is the first inserted memo."

def test_delete_one():
	_id = str(collection.find_one({ 'text': "This is the first inserted memo." })['_id']) 
	db_nav.delete_one(_id)
	assert collection.find_one({ 'text': "This is the first inserted memo." }) == None
	
def test_insert_order():
	timenow = arrow.utcnow();

	time1 = timenow
	db_nav.insert_one(time1.isoformat(), "This is the first inserted memo.")
	
	time2 = timenow.shift(weeks=+2)
	db_nav.insert_one(time2.isoformat(), "This is the second inserted memo.")
	
	time3 = timenow.shift(weeks=+1)
	db_nav.insert_one(time3.isoformat(), "This is the third inserted memo, but should be in 2nd place(index 1)")

	memos = db_nav.get_all()
	assert memos[1]['text'] == "This is the third inserted memo, but should be in 2nd place(index 1)"