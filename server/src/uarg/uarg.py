# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import ConfigParser

from flask import Flask, g, json, jsonify, Markup, render_template, request, session, url_for

import configuration

from views_api import api
from views_webui import web

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(web)

configuration.init(app)
configuration.logs(app)

import db

datadb = db.init_db(app.config["datadb_name"], app.config["datadb_ipaddress"] + ":" + app.config["datadb_port"])


db.add_view(datadb, "dialogues", "list_dialogues", ''' function(doc) { if(doc.type == 'dialogue') emit(doc._id, doc); } ''')

doc = datadb['_design/dialogues']
doc['language'] = 'javascript'
print json.dumps(doc)
doc_id = datadb.save(doc)

db.add_view(datadb, "utterances", "list_utterances", ''' function(doc) { doc.transcript.forEach(function(utter){ emit(utter.uid, utter); }); } ''')

app.config["datadb"] = datadb


@app.errorhandler(400)
def error_400(e):
    return abort('ko', 400, 'Bad Request: Browser (or proxy) sent something that could not be understood')

@app.errorhandler(401)
def error_401(e):
    return abort('ko', 401, 'something went wrong')

@app.errorhandler(403)
def error_403(e):
    return abort('ko', 403, 'something went wrong')

@app.errorhandler(404)
def error_404(e):
    return abort('ko', 404, 'something went wrong')

@app.errorhandler(405)
def error_405(e):
    return abort('ko', 405, 'Method Not Allowed for the requested URL')

@app.errorhandler(410)
def error_410(e):
    return abort('ko', 410, 'something went wrong')

@app.errorhandler(500)
def error_500(e):
    return abort('ko', 500, 'something went wrong')

def abort(status, statuscode, msg):
    """
    Check content type in the header and return error message in appropriate format.
    Defaults to JSON

    Should use e.g. return render_template('401.html'), 401
    when templates are ready
    """
    if 'text/html' in request.headers.get("Accept", ""):
        return Markup(str(statuscode)+" "+msg), statuscode
    else:
        return jsonify( {'status':status, 'statuscode': statuscode, 'message':msg} )


if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
    
