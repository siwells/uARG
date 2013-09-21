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

@api.route('/claim/<claim_id>', methods=['GET', 'PUT'])
@api.route('/claim', methods=['POST'])
def claim(claim_id = None):
    """
    """

    msg = None

    if request.method == 'GET':
        """
        Retrieves the claim identified by claim_id
        """
        msg = "GET /api/claim"+claim_id
        current_app.logger.info(msg)

    elif request.method == 'PUT':
        """
        Checks whether a claim matches the supplied claim_id. If so, replaces the 
        existing claim with the supplied claim JSON doc.
        """
        msg = "PUT /api/claim/"+claim_id
        current_app.logger.info(msg)

        print request.json

    elif request.method == 'POST':
        """
        Takes the supplied claim document and creates a new claim.
        Claim JSON doc must contain the following keys:
            [1] content

        Returns a response containing the UUID for the new claim
        """
        msg = "POST /api/claim"
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


