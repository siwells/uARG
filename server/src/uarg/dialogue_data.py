# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import uuid as UUID

from datetime import datetime


def new_dialogue(db, speaker, content, locution, referent = None):

    now = str(datetime.now().isoformat())
    utterance = new_utterance(1, speaker, content, locution, referent)
    doc = {"created": now, "type": "dialogue" , "transcript":[utterance]}
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


def get_dialogue_size(db, dialogue_uuid):
    """
    Return the size of the dialogue (Defined as the number of utterances in the transcript)
    """
    if dialogue_uuid in db:
        doc = db[dialogue_uuid]
        return len(doc.get('transcript'))


def get_dialogues(db):
    """
    Get a collection of dialogue uids
    """
    return [ db[_id].get('_id') for _id in db if db[_id].get('type') == "dialogue" ]


def get_utterance(db, dialogue_uuid = None, utterance_uuid = None, utterance_idx = None):
    """
    Return the utterance identified by either:
        utterance_uuid & dialogue_uuid
        utterance_idx & dialogue_uuid

        TODO: Add just utterande_uuid
    """
    doc = get_dialogue(db, dialogue_uuid)
    if doc is not None:
        transcript = doc['transcript']
        if utterance_uuid is not None:
            return [ u for u in transcript if u['uid']==utterance_uuid ]
        if utterance_idx is not None:
            d_size = get_dialogue_size(db, dialogue_uuid)
            if  utterance_idx <= d_size and utterance_idx > 0:
                return transcript[utterance_idx-1]
    

def new_utterance(idx, speaker, content, locution, referent = None):
    """
    Create a new utterance dictionary from the supplied arguments and return it to the caller
    """
    uid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())
    
    utterance = {'idx':idx, 'timestamp':now, 'uid': uid, 'speaker':speaker, 'content':content, 
        'locution':locution, 'referent':referent}

    return utterance
    
    

