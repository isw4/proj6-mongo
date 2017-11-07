"""
A class that contains a collection of wrappers for MongoDB collection navigation.
To be used in the memos project. Supported operations:

insert_one:			inserts a single memo
delete_one:			deletes a single memo
get_all:			returns a jsonifiable list of all the memos in the collection
"""

import arrow
import pymongo
from bson.objectid import ObjectId

"""
Function to humanize the dates
"""
def humanize_date(date):
	"""
	Date is internal UTC ISO format string.
	Output should be "today", "yesterday", "in 5 days", etc.
	Arrow will try to humanize down to the minute, so we
	need to catch 'today' as a special case. 

	Assume that the server is in the same time zone as the client
	"""
	try:
		"""
		'date' has no timezone attached. arrow assumes that it is in UTC,
		but we want to assume that the client is in the same TZ as the
		server. The next few lines slap the input date onto the local TZ
		"""
		parts = date.split('T')[0].split('-')
		then = arrow.utcnow().to('local')
		then = then.replace(year=int(parts[0]), month=int(parts[1]), day=int(parts[2]))
		# The server time + TZ
		now = arrow.utcnow().to('local')
		
		if then.date() == now.date():
			human = "Today"
		else: 
			human = then.humanize(now)
			if human == "in a day":
				human = "Tomorrow"
	except: 
		human = date
	return human

"""
Class to navigate the database collection
"""
class MemoNav:
	collection = None

	def __init__(self, collection):
		self.collection = collection

	def insert_one(self, date, text):
		"""
		Inserts a memo into the database. A memo has the following structure:
			type: 	description of the type of document
			date:	an ISO formatted date string
			score:	an index by which to sort the items(YYYYMMDD)
			text:	a description of the memo

		Args:
			date:	string, ISO formatted date
			text:	string, description of the memo

		Returns:
			None
		"""
		record = {"type": "dated_memo"}
		record['date'] = date
		record["score"] = date.split('T')[0].replace('-', '')
		record['text'] = text
		self.collection.insert(record)

	def delete_one(self, _id):
		"""
		Deletes a memo from the database

		Args:
			_id:	string, id number of the document in the collection

		Returns:
			True if a document was deleted
			False otherwise
		"""
		result = self.collection.delete_one({'_id': ObjectId(_id)})
		if result.deleted_count == 1:
			  return True
		else: return False


	def get_all(self):
		"""
		Returns all dated memos in the database, sorted by date, in a form that
		can be inserted directly in the 'session' object.

		Args:
			None

		Returns:
			a list of all documents in the collection, sorted by 'score'
		"""
		records = []
		for record in self.collection.find( { "type": "dated_memo" } ).sort('score', pymongo.ASCENDING):
			record['id'] = str(record['_id'])   # converts the id object into a string
			del record['_id']                   # removes the id object so it can be jsonified
			records.append(record)
		return records 
