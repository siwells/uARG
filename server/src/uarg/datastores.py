# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

def init_data_db(name, url):
    """
    Check whether the database 'name' exists on the couchdb server at url. If so, return reference to the server object. Otherwise create a new DB called name at url then return the new server object.
    
    Return: A CouchDB database object
    """   
    datadb = dict()
    global datadb
    server = couchdb.client.Server(url)

    try: 
        datadb[name] = server.create(name)
    except PreconditionFailed:
        datadb[name] = server[name]
    except:
        current_app.logger.critical( "Failed to connect to the uARG database. Is the CouchDB server running?" )
        print "Failed to connect to the uARG users database. Is the CouchDB server running?"
        exit(1)
    return datadb[name]

def init_user_db(name, url):
    """

    """
    userdb = dict()
    global userdb
    server = couhdb.client.Server(url)

    try:
        userdb[name] = server.create(name)
    except PreconditionFailed:
        userdb[name] = server[name]
    except:
        current_app.logger.critical("Failed to initialise the "+name+" DB. Is the CouchDB server running?")
        print "Failed to initialise the "+name+" DB. Is the CouchDB server running?"
        exit(1)
    return userdb[name]


def get_dialogue_db():
    return datadb[ current_app.config['datadb_name'] ]


def add_view(db, design, view, fun):
    """
    Adds view functions to the specified db by specifiying the design document, the view name & the search function
    """
    
    design_doc = { 'views': { view: { 'map': fun}}}
    
    try: 
        db["_design/"+design] = design_doc
    except ResourceConflict:
        pass
