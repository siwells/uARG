# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

def init_db(name, url):
    """
    Check whether the database 'name' exists on the couchdb server at url. If so, return reference to the server object. Otherwise create a new DB called name at url then return the new server object.
    
    Return: A CouchDB database object
    """   
    global db
    server = couchdb.client.Server(url)

    try: 
        db = server.create(name)
    except PreconditionFailed:
        db = server[name]
    except:
        current_app.logger.critical( "Failed to connect to the uARG database. Is the CouchDB server running?" )
        print "Failed to connect to the uARG users database. Is the CouchDB server running?"
        exit(1)
    return db

