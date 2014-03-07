# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import requests

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

import dataviews

db = dict()
#db_data = dict()

def init(app):
    """
    Initialise the databases & CouchDB views

    Can only initialise views once the DBs have successfully been initialised so 
    might as well do that here to ensure the right order is preserved.

    """

    datadb = add_db("dialoguedb", app.config["datadb_name"], app.config["datadb_ipaddress"], app.config["datadb_port"])
    userdb = add_db("userdb", app.config["userdb_name"], app.config["userdb_ipaddress"], app.config["userdb_port"])
    dataviews.init()

def add_db(label, name, ip, port):
    """
    Check whether the database 'name' exists on the couchdb server at url. If so, return reference to the server object. Otherwise create a new DB called name at url then return the new server object.
    
    Return: A CouchDB database object
    """
    server = couchdb.client.Server(ip+":"+port)

    try:
        handle = { 'handle': server.create(name) }
        db[label] = handle
        db[label]['data'] = construct_db_data_dict(name, ip, port)
    except PreconditionFailed:
        handle = { 'handle': server[name] }
        db[label] = handle
        db[label]['data'] = construct_db_data_dict(name, ip, port)
    except:
        current_app.logger.critical( "Failed to connect to the uARG "+name+" database. Is the CouchDB server running?" )
        print "Failed to connect to the uARG "+name+" database. Is the CouchDB server running?"
        exit(1)

    return db[label]


def construct_db_data_dict(name, ip, port):
    """
    Return a dict containing the supplied Key:Value pairs for the supplied name, ip, and port
    """
    data = {'ip':ip, 'port':port, 'name':name}
    return data
    


def get_dialogue_db():
    """
    Return the dialogue DB
    """
    return db['dialoguedb']['handle']


def get_dialogue_db_connection_data():
    """
    Return a dictionary contain key:value pairs for IP, Port, and DB Name
    """
    return db_data['dialoguedb']['data']


def get_user_db():
    """
    Return the user DB
    """
    return db['userdb']['handle']


def get_user_db_connection_data():
    """
    Return a dictionary containing key:value pairs for IP, Port, & DB name for the user DB
    """
    return db_data['userdb']['data']



