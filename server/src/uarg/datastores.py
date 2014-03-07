# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import requests

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
    add_view(datadb, "dialogues", "list_dialogues2", ''' function(doc) { if(doc.type == 'dialogue') emit(doc._id, doc); } ''')
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


def add_view(db, design, view, mapfun, reducefun=None):
    """
    Adds view functions to the specified db by specifiying the design document, the view name & the map/reduce functions
    """

    design_doc = get_design(db, design)
    if design_doc is None:
        if reducefun is not None:
            design_doc = { 'language':'javascript', 'views': { view: { 'map': mapfun, 'reduce': reducefun}}}
        else:
            design_doc = { 'language':'javascript', 'views': { view: { 'map': mapfun }}}
    
        try: 
            db["_design/"+design] = design_doc
        except ResourceConflict:
            pass
    else:
        if not contains_view(design_doc, view):
            fun = { 'map': mapfun }
            design_doc['views'][view] = fun
            try: 
                db["_design/"+design] = design_doc
            except ResourceConflict:
                pass


def get_design(db, design):
    """
    Get the design document from the specified DB
    
    Returns either the design document or else None
    """
    try:
        doc = db["_design/"+design]
        return doc
    except ResourceNotFound: 
        return None
    except:
        return None


def contains_view(design_doc, view_name):
    """
    Check whether the supplied design_doc contains the nominated view

    True if the design contains the view, False otherwise
    """

    if design_doc is not None:
        key = None
        try:
            key = design_doc['views'][view_name]
            if key is not None:
                return True
        except KeyError:
            return False


def call_view(db_data, design, view, limit=None, skip=None):
    """
    Call the view in the design document on the DB identified by db_data

    db_data is a dictionary containg {IP, port, name}
    design should be the name of a design document in the DB identified in db_data
    view must be a view in the previously identified design document

    Returns: JSON data output by the CouchDB view
    """

    view_url = "_design/"+design+"/_view/"+view
    args = db_data["ip"] +":"+ db_data["port"] +"/"+ db_data["name"] +"/"+ view_url
    
    if limit is not None or skip is not None:
        params = "?"
        if limit is not None:
            limit_str = "limit="+str(limit)
            params = params + limit_str
        if skip is not None:
            skip_str = "skip="+str(skip)
            params = params + skip_str
        print params

    return requests.get( args ).text
    

def list_dialogues_view(limit=None, skip=None):
    """
    Call the list dialogues view in the dialogue design document on the data DB
    """
    db_data = get_dialogue_db_connection_data()
    r = call_view(db_data, "dialogues", "list_dialogues", limit, skip)
    return r


def get_dialogue_db():
    """
    Return the dialogue DB
    """
    return db[ current_app.config['datadb_name'] ]


def get_dialogue_db_connection_data():
    """
    Return a dictionary contain key:value pairs for IP, Port, and DB Name
    """
    return {'ip':current_app.config["datadb_ipaddress"], 'port':current_app.config["datadb_port"], 'name':current_app.config["datadb_name"]}


def get_user_db():
    """
    Return the user DB
    """
    return db[ current_app.config['userdb_name'] ]


def get_user_db_connection_data():
    """
    Return a dictionary containing key:value pairs for IP, Port, & DB name for the user DB
    """
    return {'ip':current_app.config["userdb_ipaddress"], 'port':current_app.config["userdb_port"], 'name':current_app.config["userdb_name"]}

