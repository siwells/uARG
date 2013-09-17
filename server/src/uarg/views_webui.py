# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

from flask import Blueprint, json, jsonify, Markup

web = Blueprint("web", __name__, template_folder="templates", static_folder="static")

@web.route('/')
def root():
    """
    """
    
    return Markup('<strong>Hello World</strong>')

