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


def add_utterance(db, speaker, referent, content, locution):
    """

    """
    uid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())

    doc = db[referent]

    idx = len(doc['transcript']) + 1

    utterance = {'idx':idx, 'timestamp':now, 'uid': uid, 'speaker':speaker, 'referent': referent, 'content':content, 'locution':locution }

    doc['transcript'].append(utterance)
    doc_id = db.save(doc)


def get_dialogue(db, dialogue_uuid):
    """
    Get the document from db identified by event_uuid
    """
    if dialogue_uuid in db:
        return db[dialogue_uuid]


def new_utterance(idx, speaker, content, locution, referent = None):
    """

    """
    uid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())
    
    utterance = {'idx':1, 'timestamp':now, 'uid': uid, 'speaker':speaker, 'content':content, 'locution':locution}

    if ( referent is not None):
        utterance['referent'] = referent

    return utterance
    
    

