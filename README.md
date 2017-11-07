# proj6-mongo
### Author: Isaac Hong Wong(iwong@uoregon.edu)

Simple list of dated memos kept in MongoDB database

## What is here

A simple Flask app that displays all the dated memos it finds in a MongoDB database.
The web app allows a user to add and delete memos from the database.

## What goes in the credentials.ini config file

- DB : The name of your MongoDB database, which may include multiple collections
- DB_USER : A use name for your application.  
- DB_USER_PW : The password your application gives to access your database
- DB_HOST : The host computer on which your MongoDB database runs.  This
might be 'localhost' or it might be something like ds884198.mlab.com
- DB_PORT : The network port on which your MongoDB database listens.
  If you run MongoDB on your own computer, the default is 27017.  If
  you run MongoDB on MLab or a similar cloud service, it will be a port
  assigned by your cloud service. 

## Functionality

Adding dated memos
Displayed in date order
Deleting memos

## Setting up

Mlab