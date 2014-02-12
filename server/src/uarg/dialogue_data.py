# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import uuid as UUID

from datetime import datetime


def new_dialogue(db, speaker, speaker_uuid, root_txt, root_type, src_txt = None, src_url = None):

    utterance_uuid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())

    utterance = {'index':1, 'timestamp':now, 'utterance_uuid': utterance_uuid, 'speaker':speaker, 'speaker_uuid':speaker_uuid, 'content':root_txt, 'root_type':root_type}

    if (src_txt is not None and src_url is not None):
        utterance['src_txt'] = src_txt
        utterance['src_url'] = src_url
    
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
    

