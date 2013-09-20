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
        msg = "GET /api/claim"+claim_id
        current_app.logger.info(msg)

    elif request.method == 'PUT':
        msg = "PUT /api/claim/"+claim_id
        current_app.logger.info(msg)

    elif request.method == 'POST':
        msg = "POST /api/claim"
        current_app.logger.info(msg)

        print request.json

    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    return jsonify( response )

@api.route('/claims')
def claims():
    """
    Requires support for retrieving with offset + rows
    """

    msg = "CLAIMS - Retrieve claims from server"
    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    current_app.logger.warn("CLAIMS ROUTE")

    return jsonify( response )


