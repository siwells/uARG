# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Blueprint, current_app, json, jsonify, request
api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/')
def root():
    """
    """
    response_msg = "GET /api/ - This should return basic information about using the API from this route onwards"
    response = {'status':'ok', 'statusCode': 200, 'message':response_msg}

    current_app.logger.warn( response )

    return jsonify( response )

@api.route('/dialogue/<dialogue_id>', methods=['GET'])
@api.route('/dialogue', methods=['POST'])
def dialogue(dialogue_id = None):
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
        response_msg = "GET /api/dialogue"+dialogue_id
        payload = { 'transcript':[{'idx':'1', 'speaker':{'id':'12343212332', 'name':'Simon Wells'}, 'msg':'bees are nice', 'msg_type':'claim'}, {'idx':'2', 'speaker':{'id':'32143212223', 'name':'Thomas Wells'}, 'msg':'yes they are', 'msg_type':'agree'}]}


    elif request.method == 'POST':
        """
        Takes the supplied dialogue root JSON doc and creates a new dialogue.
        
        Dialogue root JSON doc must contain the following keys:
            [1] msg
            [2] type

        Returns a response containing the UUID for the new dialogue
        """
        msg = None
        msg_type = None

        data = request.json
        if all(key in data for key in ('msg','type')):
            msg = data.get('msg')
            msg_type = data.get('type')

            payload = {'dialogue_id':'DUMMYDIALOGUEID'}
            response_msg = "New dialogue created with root text 'blah blah blah'"

        elif all(key in data for key in ('resp', 'resp_txt', 'resp_type', 'src_url', 'src_txt')):
            resp = data.get('resp')
            resp_txt = data.get('resp_txt')
            resp_type = data.get('resp_type')
            src_url = data.get('src_url')
            src_txt = data.get('src_txt')
            
            payload = {'dialogue_id':'DUMMYDIALOGUEID'}
            response_msg = "New dialogue created in response to 'blah blah blah' at http://www.dkfd.com"
            

        else:
            status = 'ko'
            status_code = 400
            response_msg = "POST to /api/dialogue failed to create a new dialogue. The minimum required keys were not provided"

        
    response = {'status':status, 'status_code': status_code, 'message':response_msg, 'data':payload}
    current_app.logger.info(response)

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


