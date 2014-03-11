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

            doc_id =  dialogue_data.new_dialogue("3298h3hiu3h2u", content, locution, referent)
            
            payload['uid'] = doc_id
            payload['txt'] = content

            
            response_msg = "New dialogue created"

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
    _links = { "self": { "href": url_for('.dialogue_id', dialogue_id=dialogue_id, _external=True) }}
    
    if request.method == 'GET':
        """
        Retrieves the dialogue identified by dialogue_id
        """
        response_msg = "GET /api/dialogue/"+dialogue_id
        dialogue = dialogue_data.get_dialogue(dialogue_id)
        
        if dialogue is not None:
            for u in dialogue['transcript']:
                url = url_for('.utterance_id', dialogue_id=dialogue_id, utterance_id=u['uid'], _external=True) 
                u.update({ "_links": { "self": { "href":url }}})


        payload = dialogue

        if payload is None:
            status = 'ko'
            response_msg = "Failed to GET /api/dialogue/"+dialogue_id

    elif request.method == 'POST':
        """
        Adds a new utterance to the dialogue identified by dialogue_id
        """
        data = request.json
        referent = None
        if all(key in data for key in ('content','locution')):

            if 'referent' in data:
                referent = data.get('referent')
            content = data.get('content')
            locution = data.get('locution')

            dialogue_data.add_utterance(dialogue_id, "3298h3hiu3h2u", referent, content, locution)
            
            response_msg = "POST /api/dialogue/"+dialogue_id


    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload, '_links': _links}
    current_app.logger.info(response)

    return jsonify( response )


@api.route('/dialogue/<dialogue_id>/utterance/<utterance_id>', methods=['GET'])
def utterance_id(dialogue_id = None, utterance_id = None):
    """
    """
    response_msg = None
    payload = {}
    status = 'ok'
    status_code = 200
    _links = { "self": { "href": url_for('.utterance_id', dialogue_id=dialogue_id, utterance_id=utterance_id, _external=True) }}

    utterance_txt = None
    speaker = None
    timestamp = None
    response_to = None

    if request.method == 'GET':
        """
        Retrieves a specfied utterance from a specifed dialogue identified by utterance_id & dialogue_id
        """
        if utterance_id is not None and dialogue_id is not None:
            response_msg = "GET /api/dialogue/"+dialogue_id+"/utterance/"+utterance_id
            payload = dialogue_data.get_utterance(dialogue_id, utterance_id)

    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload, '_links': _links}
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
        date {since & until params to enable time periods}
        activity
    """
    errors = {}
    status_code = 200
    dialogues = dialogue_data.get_dialogues()
    dialogue_url = url_for('.dialogue', _external=True) + "/"

    data = [ {"uid": d, "_links":{ "self": {"href": dialogue_url + d }}} for d in dialogues  ]

    _links = { "self": { "href": url_for('.dialogues', _external=True) }}
    msg = "List of dialogues retrieved successfully from server"

    response = {'status':'ok', 'statusCode': status_code, 'message':msg, 'data':data, '_links': _links, 'errors': errors}
    current_app.logger.info(msg)
    return jsonify( response ), status_code


