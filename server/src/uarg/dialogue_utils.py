# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from datetime import datetime

def new_dialogue(utterance_id):
    """
    Return a new dialogue dict for storing in the dialogue DB
    """
    
    transcript = [{ "uid":utterance_id }]

    ddoc = {}
    ddoc['created'] = str(datetime.now().isoformat())
    ddoc['type'] = "dialogue"
    ddoc['transcript'] = transcript
    
    return ddoc


