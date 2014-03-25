# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import requests
import uuid as UUID

from datetime import datetime
from flask import current_app

import datastores
import dataviews
import utterances


def new_dialogue(speaker, content, locution, referent = None):
    """
    Create a new dialogue document

    Returns the uuid for the newly created document
    """
    udb = datastores.get_utterance_db()
    ddb = datastores.get_dialogue_db()

    udoc = utterances.new_utterance(speaker, content, locution, referent)
    udocid,rev = udb.save(udoc)

    now = str(datetime.now().isoformat())
    ddoc = {"created": now, "type": "dialogue" , "transcript":[ udocid ]}
    ddocid,rev = ddb.save(ddoc)
    
    return ddocid


def add_utterance(dialogue, speaker, referent, content, locution):
    """

    """
    udb = datastores.get_utterance_db()
    ddb = datastores.get_dialogue_db()

    udoc = utterances.new_utterance(speaker, content, locution, referent)
    udocid,rev = udb.save(udoc)

    ddoc = ddb[dialogue]
    ddoc['transcript'].append(udocid)
    ddocid,rev = ddb.save(ddoc)


def get_dialogue(dialogue_uuid):
    """
    Get the document from db identified by event_uuid
    """
    db = datastores.get_dialogue_db()
    if dialogue_uuid in db:
        doc = db[dialogue_uuid]
        return {"uid": dialogue_uuid, "created": doc['created'], "transcript": doc['transcript']}


def get_dialogue_size(dialogue_uuid):
    """
    Return the size of the dialogue (Defined as the number of utterances in the transcript)
    """
    db = datastores.get_dialogue_db()
    if dialogue_uuid in db:
        doc = db[dialogue_uuid]
        return len(doc.get('transcript'))


def get_dialogues():
    """
    Get a collection of dialogue uids
    """
    db = datastores.get_dialogue_db()

    return [ db[_id].get('_id') for _id in db if db[_id].get('type') == "dialogue" ]


def get_dialogues_count():
    """
    Quick & dirty but terribly inefficient way to get the number of dialogues on the server ;)
    """
    #view_url = "_design/d/_view/count"
    #args = current_app.config["datadb_ipaddress"] +":"+ current_app.config["datadb_port"] +"/"+ current_app.config["datadb_name"] +"/"+ view_url
    #r = json.loads( requests.get( args ).text )
    #return r['rows'][0]['value']
    db = datastores.get_dialogue_db()
    return len( [db[_id].get('_id') for _id in db if db[_id].get('type') == "dialogue"] )


def get_utterance(dialogue_uuid = None, utterance_uuid = None):
    """
    Return the utterance identified by either:
        utterance_uuid & dialogue_uuid

        TODO: Add just utterance_uuid
    """
    doc = get_dialogue(dialogue_uuid)
    if doc is not None:
        transcript = doc['transcript']
        if utterance_uuid is not None:
            for u in transcript:
                if u['uid'] == utterance_uuid:
                    return u


