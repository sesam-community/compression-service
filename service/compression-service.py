from flask import Flask, request, Response, abort
import requests
import zlib
from sesamutils import sesam_logger
from sesamutils.flask import serve

app = Flask(__name__)
logger = sesam_logger("compression-service", app=app)


def decode_file(url):
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    with requests.get(url, stream=True) as r:
        for chunk in r.iter_content(chunk_size=1048576, decode_unicode=False):
            if chunk:
                yield d.decompress(chunk)


@app.route('/gzip', methods=['GET'])
def get_gzip():
    full_url = request.args.get('url', None)  # use default value replace 'None'
    logger.info(f"processing request for {full_url}")
    if not full_url:
        return abort(400, "Missing url param in request.")

    return Response(decode_file(full_url), mimetype='application/json', direct_passthrough=True)


if __name__ == "__main__":
    logger.info("Starting service...")
    serve(app)