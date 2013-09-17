# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import ConfigParser

from flask import Flask, json, jsonify, Markup, render_template, request, session, url_for

import configuration

from views_api import api
from views_webui import web

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(web)

configuration.init(app)
configuration.logs(app)

@app.errorhandler(401)
def error_401(e):
	#return render_template('401.html'), 401
    return Markup("401 Error"), 401

@app.errorhandler(403)
def error_403(e):
	#return render_template('403.html'), 403
    return Markup("403 Error"), 403

@app.errorhandler(404)
def error_404(e):
    if 'text/html' in request.headers.get("Accept", ""):
        return Markup("404 Error"), 404
    else:
        return jsonify( {'status':'ko', 'statusCode': 404, 'message':'something went wrong'} )

@app.errorhandler(410)
def error_410(e):
	#return render_template('410.html'), 410
    return Markup("410 Error"), 410

@app.errorhandler(500)
def error_500(e):
	#return render_template('500.html'), 500
    return Markup("500 Error"), 500

if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
    
