# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

db = dict()

def init_db(name, url):
    """
    Check whether the database 'name' exists on the couchdb server at url. If so, return reference to the server object. Otherwise create a new DB called name at url then return the new server object.
    
    Return: A CouchDB database object
    """   
    server = couchdb.client.Server(url)

    try: 
        db[name] = server.create(name)
    except PreconditionFailed:
        db[name] = server[name]
    except:
        current_app.logger.critical( "Failed to connect to the uARG database. Is the CouchDB server running?" )
        print "Failed to connect to the uARG users database. Is the CouchDB server running?"
        exit(1)
    return db[name]

def get_dialogue_db():
    return db[ current_app.config['datadb_name'] ]


def add_view(db, design, view, fun):
    """
    Adds view functions to the specified db by specifiying the design document, the view name & the search function
    """
    
    design_doc = { 'views': { view: { 'map': fun}}}
    
    try: 
        db["_design/"+design] = design_doc
    except ResourceConflict:
        pass
