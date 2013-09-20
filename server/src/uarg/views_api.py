# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Blueprint, json, jsonify, current_app

api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/')
def root():
    """
    """
    msg = "ROOT - This should return basic information about using the API from this route onwards"
    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    current_app.logger.warn("ROOT ROUTE")

    return jsonify( response )

@api.route('/claim')
def claim():
    """
    """

    msg = "CLAIM - This should return basic information about using the API from this route onwards"
    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    current_app.logger.warn("CLAIM ROUTE")

    return jsonify( response )

