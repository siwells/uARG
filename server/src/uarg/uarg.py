# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import ConfigParser

from flask import Flask, json, jsonify, render_template, request, session, url_for

import configuration

app = Flask(__name__)

configuration.init(app)
configuration.logs(app)




@app.route('/')
def root():
    msg = { 'hello':'world' }
    return jsonify( msg )


if __name__ == '__main__':
    app.run(
        host=app.config['ip_address'], 
        port=int(app.config['port']), 
        threaded=app.config['threaded'])
    
