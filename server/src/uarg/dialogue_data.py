# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import uuid as UUID

from datetime import datetime


def new_dialogue(db, speaker, content, locution, referent = None):

    uid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())

    utterance = {'idx':1, 'timestamp':now, 'uid': uid, 'speaker':speaker, 'content':content, 'locution':locution}

    if ( referent is not None):
        utterance['referent'] = referent
    
    doc = {"created": now, "transcript":[utterance]}
    doc_id = db.save(doc)


def add_utterance(db, speaker, speaker_uuid, dialogue_uuid, source_uuid, response_txt, response_type):
    """

    """
    utterance_uuid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())

    doc = db[dialogue_uuid]

    idx = len(doc['transcript']) + 1

    utterance = {'index':idx, 'timestamp':now, 'utterance_uuid': utterance_uuid, 'speaker':speaker, 'speaker_uuid':speaker_uuid, 'source_uuid': source_uuid, 'content':response_txt, 'response_type':response_type }

    doc['transcript'].append(utterance)
    doc_id = db.save(doc)


def get_dialogue(db, dialogue_uuid):
    """
    Get the document from db identified by event_uuid
    """
    if dialogue_uuid in db:
        return db[dialogue_uuid]
    

