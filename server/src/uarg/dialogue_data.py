# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json
import uuid as UUID

from datetime import datetime

def new_dialogue(db, speaker, speaker_uuid, root_txt, root_type):

    dialogue_uuid = str(UUID.uuid4())
    utterance_uuid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())

    utterance = {'index':0, 'timestamp':now, 'utterance_uuid': utterance_uuid, 'speaker':speaker, 'speaker_uuid':speaker_uuid, 'content':root_txt, 'root_type':root_type}
    
    doc = {"dialogue_uuid": dialogue_uuid, "created": now, "transcript":[utterance]}
    doc_id = db.save(doc)

def add_utterance(db):
    """

    """

def get_dialogue(db, dialogue_id):
    """
    Get the document from db identified by event_uuid
    """
    if dialogue_id in db:
        return db[dialogue_id]
    

