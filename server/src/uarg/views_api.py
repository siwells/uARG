# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Blueprint, current_app, json, jsonify, request
api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/')
def root():
    """
    """
    msg = "GET /api/ - This should return basic information about using the API from this route onwards"
    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    current_app.logger.warn("GET /api/")

    return jsonify( response )

@api.route('/dialogue/<dialogue_id>', methods=['GET'])
@api.route('/dialogue', methods=['POST'])
def dialogue(dialogue_id = None):
    """
    """

    msg = None

    if request.method == 'GET':
        """
        Retrieves the dialogue identified by dialogue_id
        """
        msg = "GET /api/dialogue"+dialogue_id
        current_app.logger.info(msg)


    elif request.method == 'POST':
        """
        Takes the supplied dialogue root JSON doc and creates a new dialogue.
        
        Dialogue root JSON doc must contain the following keys:
            [1] root_msg
            [2] root_msg_type

        Returns a response containing the UUID for the new dialogue
        """
        msg = "POST /api/dialogue"
        current_app.logger.info(msg)

        print request.json

    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    return jsonify( response )

@api.route('/dialogues')
def dialogues():
    """
    Requires support for retrieving with offset + rows
    """

    msg = "DIALOGUES - Retrieve claims from server"
    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    current_app.logger.info(msg)

    return jsonify( response )


