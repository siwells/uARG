# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import couchdb
import json

def new_dialogue(db, root_txt, root_type):
    doc = {"root_txt": root_txt, "root_type": root_type}
    doc_id = db.save(doc)
