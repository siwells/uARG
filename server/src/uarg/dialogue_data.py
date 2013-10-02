# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json

from datetime import datetime

def new_dialogue(db, speaker, speaker_uuid, root_txt, root_type):

    now = str(datetime.now().isoformat())
    
    doc = {"created": now, "transcript":[]}
    doc_id = db.save(doc)
