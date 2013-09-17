# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import ConfigParser

from flask import Flask, json, jsonify, render_template, request, session, url_for

import configuration

from api.views import api
from webui.views import web

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(web)


configuration.init(app)
configuration.logs(app)


if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
    
