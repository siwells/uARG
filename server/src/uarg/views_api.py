# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Blueprint, current_app, json, jsonify, request, url_for
api = Blueprint("api", __name__, url_prefix='/api')

import dialogue_data
import responses

@api.route('/')
def root():
    """
    """
    errors = []
    data = []
    status = 'ok'
    code = 200
    _links = responses.assemble_links([responses.get_link('self', url_for('.root', _external=True) )])
    msg = "GET /api/ - This should return basic information about using the API from this route onwards"
    response = responses.build_response(msg, status, code, data, errors, _links)
    current_app.logger.info( response )
    return jsonify( response ), code


@api.route('/dialogue', methods=['POST'])
def dialogue(dialogue_id = None):
    """
    """
    errors = []
    msg = None
    data = {}
    status = 'ok'
    code = 200
    _links = responses.assemble_links([responses.get_link('self', url_for('.dialogue', _external=True) )])

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
        payload = request.json
        if 'content' in payload:
            content = payload.get('content')
            if 'locution' in payload:
                locution = payload.get('locution')
            else:
                locution = "claim"

            referent = None
            if 'referent' in payload:
                referent = payload.get('referent')

            doc_id =  dialogue_data.new_dialogue("3298h3hiu3h2u", content, locution, referent)
            
            data['uid'] = doc_id
            data['txt'] = content
            url = url_for('.dialogue_id', dialogue_id=doc_id, _external=True)
            data['_links'] = responses.assemble_links([responses.get_link('self', url )])

            
            msg = "New dialogue created"

        else:
            status = 'ko'
            code = 400
            response_msg = "POST to /api/dialogue failed to create a new dialogue. The minimum required keys were not provided"
    
    response = responses.build_response(msg, status, code, data, errors, _links)
    current_app.logger.info(response)

    return jsonify( response ), code


@api.route('/dialogue/<dialogue_id>', methods=['GET','POST'])
def dialogue_id(dialogue_id = None):
    """
    """
    errors = []
    msg = None
    data = {}
    status = 'ok'
    code = 200
    _links = responses.assemble_links([responses.get_link('self', url_for('.dialogue_id', dialogue_id=dialogue_id, _external=True) )])
    
    if request.method == 'GET':
        """
        Retrieves the dialogue identified by dialogue_id
        """
        msg = "GET /api/dialogue/"+dialogue_id
        data = dialogue_data.get_dialogue(dialogue_id)
        
        if data is not None:
            for u in data['transcript']:
                url = url_for('.utterance_id', dialogue_id=dialogue_id, utterance_id=u['uid'], _external=True)
                link = responses.assemble_links([responses.get_link('self', url )])
                u.update( { "_links": link } )
            msg = "Retrieved Dialogue #"+dialogue_id

        else:
            status = 'ko'
            msg = "Failed to GET /api/dialogue/"+dialogue_id

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
            
            msg = "POST /api/dialogue/"+dialogue_id

    response = responses.build_response(msg, status, code, data, errors, _links)
    current_app.logger.info(response)

    return jsonify( response ), code


@api.route('/dialogue/<dialogue_id>/utterance/<utterance_id>', methods=['GET'])
def utterance_id(dialogue_id = None, utterance_id = None):
    """
    """
    errors = []
    msg = None
    data = {}
    status = 'ok'
    code = 200

    _links = responses.assemble_links([responses.get_link('self', url_for('.utterance_id', dialogue_id=dialogue_id, utterance_id=utterance_id, _external=True) )])

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
            utterance = dialogue_data.get_utterance(dialogue_id, utterance_id)
            if utterance is not None:
                data = utterance
                msg = "Retrieved utterance #"+utterance_id

    response = responses.build_response(msg, status, code, data, errors, _links)
    current_app.logger.info( response )

    return jsonify( response ), code


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
    errors = []
    status = 'ok'
    code = 200
    dialogues = dialogue_data.get_dialogues()
    dialogue_url = url_for('.dialogue', _external=True) + "/"

    data = [ {"uid": d, "_links": responses.assemble_links([ responses.get_link('self', dialogue_url + d) ]) } for d in dialogues  ]
    _links = responses.assemble_links([responses.get_link('self', url_for('.dialogues', _external=True) )])
    msg = "List of dialogues retrieved successfully from server"

    response = responses.build_response(msg, status, code, data, errors, _links)

    current_app.logger.info(msg)
    return jsonify( response ), code


