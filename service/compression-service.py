from flask import Flask, request, Response
import os
import cherrypy
import json
import logging
import paste.translogger
import requests
import gzip
import urllib.parse

app = Flask(__name__)

logger = logging.getLogger("compression-service")

# settings dependent on environment variables
SERVICE_URL = os.environ.get("SERVICE_URL", "")

@app.route('/', methods=['GET'])
def root():
    return Response(status=200, response="Working.")

@app.route('/gzip/<path>', methods=['GET'])
def get_gzip(path):

    def get_file(url):
        headers = {
            'Content-Type': 'application/json'
            }
        data = requests.get(url, headers=headers, stream=True)

        if data.status_code == 200:
            data.raw.decode_content = True  # just in case transport encoding was applied
        return gzip.GzipFile(fileobj=data.raw)

    full_url = SERVICE_URL + urllib.parse.unquote(path)
    return Response(get_file(full_url), mimetype='application/json')


if __name__ == '__main__':
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Log to stdout, change to or add a (Rotating)FileHandler to log to a file
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(stdout_handler)

    # Comment these two lines if you don't want access request logging
    app.wsgi_app = paste.translogger.TransLogger(app.wsgi_app, logger_name=logger.name,
                                                 setup_console_handler=False)
    app.logger.addHandler(stdout_handler)

    logger.propagate = False
    logger.setLevel(logging.INFO)

    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5001,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


