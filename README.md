# proj6-mongo
### Author: Isaac Hong Wong(iwong@uoregon.edu)

Simple list of dated memos kept in a MongoDB database

## What is here

A simple Flask app that displays all the dated memos it finds in a MongoDB database.
The web app allows a user to add and delete memos from the database. 

## Functionality

Adding dated memos
Displayed in date order
Deleting memos

## Setting up

It's recommended to use Mlab to host the database. Other configurations are not supported.

1) Be in the outermost directory. Copy credentials-skel.ini to memos/credentials.ini

```
cp credentials-skel.ini memos/credentials.ini
```

2) Fill out the fields as directed below
3) From the outermost directory, run:

```
make install
make run
```

4) ctrl-c to stop the server

### What goes in the credentials.ini config file

- SECRET_KEY : The secret key used to encrypt Flask session cookies. Not really necessary for this app
- PORT : The port number on which to serve your Flask app
- DB : The name of your MongoDB database, which may include multiple collections
- DB_COLLECTION = collection within database
- DB_USER : A user name for your application.  
- DB_USER_PW : The password your application gives to access your database
- DB_HOST : The host computer on which your MongoDB database runs.  This
might be 'localhost' or it might be something like ds884198.mlab.com
- DB_PORT : The network port on which your MongoDB database listens.
  If you run MongoDB on your own computer, the default is 27017.  If
  you run MongoDB on MLab or a similar cloud service, it will be a port
  assigned by your cloud service.