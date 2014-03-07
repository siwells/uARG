# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import requests

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

import dataviews

db = dict()
db_data = dict()

def init(app):
    """
    Initialise the databases & CouchDB views

    Can only initialise views once the DBs have successfully been initialised so 
    might as well do that here to ensure the right order is preserved.

    """

    datadb = add_db("dialoguedb", app.config["datadb_name"], app.config["datadb_ipaddress"] + ":" + app.config["datadb_port"])
    db_data['dialoguedb'] = {   'ip':app.config["datadb_ipaddress"], 
                                'port':app.config["datadb_port"], 
                                'name':app.config["datadb_name"]}

    userdb = add_db("userdb", app.config["userdb_name"], app.config["userdb_ipaddress"] + ":" + app.config["userdb_port"])
    db_data['userdb'] = {   'ip':app.config["userdb_ipaddress"], 
                                'port':app.config["userdb_port"], 
                                'name':app.config["userdb_name"]}
    dataviews.init()

def add_db(label, name, url):
    """
    Check whether the database 'name' exists on the couchdb server at url. If so, return reference to the server object. Otherwise create a new DB called name at url then return the new server object.
    
    Return: A CouchDB database object
    """   
    server = couchdb.client.Server(url)

    try: 
        db[label] = server.create(name)
    except PreconditionFailed:
        db[label] = server[name]
    except:
        current_app.logger.critical( "Failed to connect to the uARG "+name+" database. Is the CouchDB server running?" )
        print "Failed to connect to the uARG "+name+" database. Is the CouchDB server running?"
        exit(1)

    return db[label]


def get_dialogue_db():
    """
    Return the dialogue DB
    """
    return db[ 'dialoguedb' ]


def get_dialogue_db_connection_data():
    """
    Return a dictionary contain key:value pairs for IP, Port, and DB Name
    """
    return db_data[ 'dialoguedb' ]


def get_user_db():
    """
    Return the user DB
    """
    return db[ 'userdb' ]


def get_user_db_connection_data():
    """
    Return a dictionary containing key:value pairs for IP, Port, & DB name for the user DB
    """
    return db_data[ 'userdb' ]



