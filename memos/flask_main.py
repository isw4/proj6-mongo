"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

import sys

# Date handling 
import arrow   
from dateutil import tz  # For interpreting local times

# Mongo database
from pymongo import MongoClient
from bson.objectid import ObjectId

import config
CONFIG = config.configuration()


MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST, 
    CONFIG.DB_PORT, 
    CONFIG.DB)


print("Using URL '{}'".format(MONGO_CLIENT_URL))


###
# Globals
###

app = flask.Flask(__name__)
app.secret_key = CONFIG.SECRET_KEY

####
# Database connection per server process
###

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    collection = getattr(db, CONFIG.DB_COLLECTION)

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  g.memos = get_memos()
  for memo in g.memos: 
      app.logger.debug("Memo: " + str(memo))
  return flask.render_template('index.html')


@app.route("/create", methods=["GET"])
def create_page():
    app.logger.debug("Create memo page sent")
    return flask.render_template('create.html')


@app.route("/create", methods=["POST"])
def create_submit():
    app.logger.debug("Create memo request received by server")
    req_date = request.form['date-input']
    req_text = request.form['text-input']
    if req_date == None or req_text == None:
      app.logger.debug('Request inputs not complete')
      Flask.flash('Request inputs not complete. Memo not created.')
    else:
      app.logger.debug('Inserting memo into db')
      create_memo(req_date, req_text)
    return flask.redirect(url_for('index'))


@app.route("/delete", methods=["POST"])
def delete_submit():
    app.logger.debug("Delete memo request received by server")
    app.logger.debug("request.form: {}".format(request.form))

    result = {}
    if request.form.get('id', None, type=str) == None:
      app.logger.debug("No memo id included")
      result = {'exception': 'No memo id included'}
    else:
      app.logger.debug("Memo id to be deleted is: {}".format(request.form.get('id')))
      deleted = delete_memo(request.form.get('id'))
      if not deleted:
        result = {'exception': 'Error in deleting entry'}
    return flask.jsonify(result=result)


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case. 
    """
    try:
        then = arrow.get(date).to('local')
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


#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['id'] = str(record['_id'])   # converts the id object into a string
        del record['_id']                   # removes the id object so it can be jsonified
        records.append(record)
    return records 


def create_memo(date, text):
    """ Inserts a memo into the database """
    record = {"type": "dated_memo"}
    record['date'] = date
    record['text'] = text
    collection.insert(record)


def delete_memo(_id):
    """ Deletes a memo from the database """
    result = collection.delete_one({'_id': ObjectId(_id)})
    if result.deleted_count == 1:
          return True
    else: return False


if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")