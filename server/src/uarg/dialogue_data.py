# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import uuid as UUID

from datetime import datetime


def new_dialogue(db, speaker, content, locution, referent = None):

    now = str(datetime.now().isoformat())
    utterance = new_utterance(1, speaker, content, locution, referent)
    doc = {"created": now, "transcript":[utterance]}
    doc_id = db.save(doc)


def add_utterance(db, dialogue, speaker, referent, content, locution):
    """

    """
    doc = db[dialogue]
    idx = len(doc['transcript']) + 1
    utterance = new_utterance(idx, speaker, content, locution, referent)
    doc['transcript'].append(utterance)
    doc_id = db.save(doc)


def get_dialogue(db, dialogue_uuid):
    """
    Get the document from db identified by event_uuid
    """
    if dialogue_uuid in db:
        doc = db[dialogue_uuid]
        return {"uid": dialogue_uuid, "created": doc['created'], "transcript": doc['transcript']}

def get_dialogues(db):
    """
    Get a collection of dialogue uids
    """

    return [ db[_id].get('_id') for _id in db ]

def get_utterance(db, dialogue_uuid, utterance_uuid):
    """
    Return the utterance identified by utterance_uuid & dialogue_uuid
    """
    doc = get_dialogue(db, dialogue_uuid)
    if doc is not None:
        transcript = doc['transcript']
        return [ u for u in transcript if u['uid']==utterance_uuid ]

def new_utterance(idx, speaker, content, locution, referent = None):
    """
    Create a new utterance dictionary from the supplied arguments and return it to the caller
    """
    uid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())
    
    utterance = {'idx':idx, 'timestamp':now, 'uid': uid, 'speaker':speaker, 'content':content, 
        'locution':locution, 'referent':referent}

    return utterance
    
    

