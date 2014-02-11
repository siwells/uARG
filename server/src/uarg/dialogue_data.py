# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json

from datetime import datetime

def new_dialogue(db, speaker, speaker_uuid, root_txt, root_type):

    now = str(datetime.now().isoformat())

    utterance = {'timestamp':now, 'speaker':speaker, 'speaker_uuid':speaker_uuid, 'content':root_txt, 'root_type':root_type}
    print json.dumps(utterance)
    
    doc = {"created": now, "transcript":[utterance]}
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
    

