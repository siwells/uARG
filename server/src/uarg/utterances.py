# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import uuid as UUID

from datetime import datetime

def new_utterance(speaker, content, locution, referent = None):
    """
    Create a new utterance dictionary from the supplied arguments and return it to the caller
    """
    uid = str(UUID.uuid4())
    now = str(datetime.now().isoformat())
    
    utterance = {'timestamp':now, 'speaker':speaker, 'content':content, 
        'locution':locution, 'referent':referent}

    return utterance
