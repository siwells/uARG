# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

db = dict()

def init(app):
    """
    Initialise the databases & CouchDB views
    """

    datadb = add_db(app.config["datadb_name"], app.config["datadb_ipaddress"] + ":" + app.config["datadb_port"])
    userdb = add_db(app.config["userdb_name"], app.config["userdb_ipaddress"] + ":" + app.config["userdb_port"])

    add_view(datadb, "dialogues", "list_dialogues", ''' function(doc) { if(doc.type == 'dialogue') emit(doc._id, doc); } ''')
    add_view(datadb, "utterances", "list_utterances", ''' function(doc) { doc.transcript.forEach(function(utter){ emit(utter.uid, utter); }); } ''')


def add_db(name, url):
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
        current_app.logger.critical( "Failed to connect to the uARG "+name+" database. Is the CouchDB server running?" )
        print "Failed to connect to the uARG "+name+" database. Is the CouchDB server running?"
        exit(1)
    return db[name]

def get_dialogue_db():
    """
    Return the dialogue DB
    """
    return db[ current_app.config['datadb_name'] ]

def get_user_db():
    return db[ current_app.config['userdb_name'] ]


def add_view(db, design, view, fun):
    """
    Adds view functions to the specified db by specifiying the design document, the view name & the search function
    """
    
    design_doc = { 'language':'javascript', 'views': { view: { 'map': fun}}}
    
    try: 
        db["_design/"+design] = design_doc
    except ResourceConflict:
        pass
