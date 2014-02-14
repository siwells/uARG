# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Blueprint, current_app, json, jsonify, request, url_for
api = Blueprint("api", __name__, url_prefix='/api')

import dialogue_data

@api.route('/')
def root():
    """
    """
    payload = {}
    response_msg = "GET /api/ - This should return basic information about using the API from this route onwards"
    response = {'status':'ok', 'statusCode': 200, 'message':response_msg, 'data':payload}

    current_app.logger.info( response )

    return jsonify( response )


@api.route('/dialogue', methods=['POST'])
def dialogue(dialogue_id = None):
    """
    """
    response_msg = None
    payload = {}
    status = 'ok'
    status_code = 200

    if request.method == 'POST':
        """
        Takes the supplied dialogue root JSON doc and creates a new dialogue. 
        
        2 types of dialogue root are allowed: 
            [1] a root created by the user
            [2] a root in respose to an existing resource that is identified by URL
        
        A type 1 root JSON doc must contain the following keys:
            [1] msg
            [2] msg_type

        A type 2 root JSON doc must contain the following keys:
            [1] resp_txt
            [2] resp_type
            [3] src_url
            [4] src_txt

        Returns a response containing the UUID for the new dialogue
        """
        data = request.json
        if 'content' in data:
            content = data.get('content')
            if 'locution' in data:
                locution = data.get('locution')
            else:
                locution = "claim"

            referent = None
            if 'referent' in data:
                referent = data.get('referent')

            dialogue_data.new_dialogue(current_app.config['datadb'], "3298h3hiu3h2u", content, locution, referent)
            response_msg = "New dialogue created with root text 'blah blah blah'"

        else:
            status = 'ko'
            status_code = 400
            response_msg = "POST to /api/dialogue failed to create a new dialogue. The minimum required keys were not provided"
        
    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload}
    current_app.logger.info(response)

    return jsonify( response )


@api.route('/dialogue/<dialogue_id>', methods=['GET','POST'])
def dialogue_id(dialogue_id = None):
    """
    """
    response_msg = None
    payload = {}
    status = 'ok'
    status_code = 200

    
    if request.method == 'GET':
        """
        Retrieves the dialogue identified by dialogue_id
        """
        response_msg = "GET /api/dialogue/"+dialogue_id
        payload = dialogue_data.get_dialogue(current_app.config['datadb'], dialogue_id)
        
        if payload is None:
            status = 'ko'
            response_msg = "Failed to GET /api/dialogue/"+dialogue_id

    elif request.method == 'POST':
        """
        Adds a new utterance to the dialogue identified by dialogue_id
        """
        data = request.json
        if all(key in data for key in ('referent', 'content','locution')):

            referent = data.get('referent')
            content = data.get('content')
            locution = data.get('locution')

            dialogue_data.add_utterance(current_app.config['datadb'], dialogue_id, "3298h3hiu3h2u", referent, content, locution)
            
            response_msg = "POST /api/dialogue/"+dialogue_id


    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload}
    current_app.logger.info(response)

    return jsonify( response )


@api.route('/dialogue/<dialogue_id>/transcript/<utterance_id>', methods=['GET'])
def utterance(dialogue_id = None, utterance_id = None):
    """
    """
    response_msg = None
    payload = {}
    status = 'ok'
    status_code = 200

    utterance_txt = None
    speaker = None
    timestamp = None
    response_to = None

    if request.method == 'GET':
        """
        Retrieves a specfied utterance from a specifed dialogue identified by utterance_id & dialogue_id
        """
        response_msg = "GET /api/dialogue/"+dialogue_id+"/transcript/"+utterance_id
        payload = { 'dialogue_id':dialogue_id, 'utterance_id':utterance_id, 'utterance_txt':utterance_txt, 'speaker':speaker, 'timestampt':timestamp, 'response_to':response_to }

    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload}
    current_app.logger.info( response )

    return jsonify( response )


@api.route('/dialogue/<dialogue_id>/transcript/<utterance_id>/response', methods=['POST'])
def response(dialogue_id = None, utterance_id = None):
    """
    """
    response_msg = None
    payload = {}
    status = 'ok'
    status_code = 200

    utterance_txt = None
    speaker = None
    timestamp = None
    response_to = None

    if request.method == 'POST':
        """
        Post an utterance to the specified dialogue identified by dialogue_id
        """
        data = request.json
        if all(key in data for key in ('msg_txt','msg_type')):
            msg_txt = data.get('msg_txt')
            msg_type = data.get('msg_type')
            
            response_msg = "POST /api/dialogue/"+dialogue_id+"/transcript/"+utterance_id+"/response"
            payload = {'dialogue_id':'DUMMYDIALOGUEID', 'utterance_id':'NEWDUMMYUTTERANCEID', 'in_response_to':utterance_id}

        else:
            status = 'ko'
            status_code = 400
            response_msg = "POST to /api/dialogue failed to create a new dialogue. The minimum required keys were not provided"

    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload}
    current_app.logger.info( response )

    return jsonify( response )


@api.route('/dialogue/<dialogue_id>/transcript/<utterance_id>/responses', methods=['GET'])
def responses(dialogue_id = None, utterance_id = None):
    """
    """
    response_msg = None
    payload = {}
    status = 'ok'
    status_code = 200

    utterance_txt = None
    speaker = None
    timestamp = None
    response_to = None

    if request.method == 'GET':
        response_msg = "GET /api/dialogue/"+dialogue_id+"/transcript/"+utterance_id+"/responses"
        payload = {'dialogue_id':'DUMMYDIALOGUEID', 'utterance_id':'DUMMYUTTERANCEID', 'responses':[{'utterance_id':'9237498321', 'utterance_txt':'blah blah blah', 'time_stamp':None}]}

    else:
        status = 'ko'
        status_code = 400
        response_msg =  "GET /api/dialogue/"+dialogue_id+"/transcript/"+utterance_id+"/responses failed."

    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload}
    current_app.logger.info( response )

    return jsonify( response )


@api.route('/dialogues')
def dialogues():
    """
    Requires support for retrieving with the following arguments:
        count
        offset
        user_id
        order
        tags
        ratings
        date
        activity
    """
    dialogues = dialogue_data.get_dialogues(current_app.config['datadb'])
    url = url_for('.dialogues', _external=True)
    payload = [ {"uid": d, "link": url + d }  for d in dialogues  ]
        
    msg = "List of dialogues retrieved successfully from server"
    response = {'status':'ok', 'statusCode': 200, 'message':msg, 'data':payload}
    current_app.logger.info(msg)
    return jsonify( response )


