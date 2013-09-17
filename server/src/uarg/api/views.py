# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Blueprint, json, jsonify

api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/log')
def log():
    """
    """

    msg = "LOGS"
    response = {'status':'ok', 'statusCode': 200, 'message':msg}

    return jsonify( response )
