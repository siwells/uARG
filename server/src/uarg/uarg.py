# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Flask, json, jsonify, render_template, request, session, url_for


app = Flask(__name__)


@app.route('/')
def root():
    msg = { 'hello':'world' }
    return jsonify( msg )


if __name__ == '__main__':
    app.run()
    
