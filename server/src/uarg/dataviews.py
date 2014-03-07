# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import requests

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict
from flask import current_app

import datastores

def init():
    """

    """
    datadb = datastores.get_dialogue_db()
    userdb = datastores.get_user_db()

    add_view(datadb, "dialogues", "list", ''' function(doc) { if(doc.type == 'dialogue') emit(doc._id, doc); } ''')
    add_view(datadb, "dialogues", "count", ''' function(doc) { if(doc.type == 'dialogue') emit(doc._id, doc); } ''', '''_count''')
    add_view(datadb, "utterances", "list_utterances", ''' function(doc) { doc.transcript.forEach(function(utter){ emit(utter.uid, utter); }); } ''')


def add_view(db, design, view, mapfun, reducefun=None):
    """
    Adds view functions to the specified db by specifiying the design document, the view name & the map/reduce functions
    """

    design_doc = get_design(db, design)
    if design_doc is None:
        design_doc = construct_designdoc(view, mapfun, reducefun)    
        try: 
            db["_design/"+design] = design_doc
        except ResourceConflict:
            pass
    else:
        if not contains_view(design_doc, view):
            fun = construct_mapreduce(mapfun, reducefun)
            design_doc['views'][view] = fun
            try: 
                db["_design/"+design] = design_doc
            except ResourceConflict:
                pass


def construct_designdoc(view, mapfun, reducefun=None):
    """
    Construct a dict that represents a CouchDB design doc

    Returns a CouchDB design doc
    """
    design_doc = {}
    design_doc['language'] = 'javascript'
    design_doc['views'] = construct_view(view, mapfun, reducefun)
    return design_doc


def construct_view(view, mapfun, reducefun=None):
    """
    Construct a dict representing a single view ready for inclusion in a CouchDB design doc

    Returns a dict representing the CouchDB view function
    """
    viewstring = {}
    viewstring[view] = construct_mapreduce(mapfun, reducefun)
    return viewstring


def construct_mapreduce(mapfun, reducefun=None):
    """
    Construct the dict that encapsulates the map & (optionally) reduce functions

    Returns a dict representing the map/reduce functions for a couchdb view
    """
    fun = {}
    fun['map'] = mapfun
    if reducefun is not None:
        fun['reduce'] = reducefun
    return fun


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
    db_data = datastores.get_dialogue_db_connection_data()
    r = call_view(db_data, "dialogues", "list", limit, skip)
    return r







