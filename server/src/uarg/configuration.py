# coding: utf-8
# as per http://www.python.org/dev/peps/pep-0263/

import ConfigParser
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)
        
        app.config['DEBUG'] = config.get("daybook", "debug")
        app.config['threaded'] = config.get("daybook", "threaded")
        app.config['SECRET_KEY'] = config.get("daybook", "secret_key")
        app.config['ip_address'] = config.get("daybook", "ip_address")
        app.config['port'] = config.get("daybook", "port")
        app.config['url'] = config.get("daybook", "url")

        app.config['userdb_name'] = config.get("userdb", "name")
        app.config['userdb_ipaddress'] = config.get("userdb", "ip_address")
        app.config['userdb_port'] = config.get("userdb", "port")

        app.config['dialoguedb_name'] = config.get("dialoguedb", "name")
        app.config['dialoguedb_ipaddress'] = config.get("dialoguedb", "ip_address")
        app.config['dialoguedb_port'] = config.get("dialoguedb", "port")

        app.config['utterancedb_name'] = config.get("utterancedb", "name")
        app.config['utterancedb_ipaddress'] = config.get("utterancedb", "ip_address")
        app.config['utterancedb_port'] = config.get("utterancedb", "port")

        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")
    except:
        print "Could not read configs from: ", config_location

def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024* 1024 * 10 , backupCount=1024)
    file_handler.setLevel( app.config['log_level'] )
    formatter = logging.Formatter("%(levelname)s | %(asctime)s |  %(module)s | %(funcName)s | %(message)s")
    file_handler.setFormatter(formatter)

    rootLogger = logging.getLogger()
    rootLogger.setLevel( app.config['log_level'] )
    rootLogger.addHandler(file_handler)

    app.logger.setLevel( app.config['log_level'] )
    app.logger.addHandler(file_handler)
