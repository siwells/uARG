# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import requests

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

import dataviews

db = dict()

def init(app):
    """
    Initialise the databases & CouchDB views
    """

    datadb = add_db(app.config["datadb_name"], app.config["datadb_ipaddress"] + ":" + app.config["datadb_port"])
    userdb = add_db(app.config["userdb_name"], app.config["userdb_ipaddress"] + ":" + app.config["userdb_port"])
    
    dataviews.add_view(datadb, "dialogues", "list", ''' function(doc) { if(doc.type == 'dialogue') emit(doc._id, doc); } ''')
    dataviews.add_view(datadb, "dialogues", "count", ''' function(doc) { if(doc.type == 'dialogue') emit(doc._id, doc); } ''', '''_count''')
    dataviews.add_view(datadb, "utterances", "list_utterances", ''' function(doc) { doc.transcript.forEach(function(utter){ emit(utter.uid, utter); }); } ''')


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

