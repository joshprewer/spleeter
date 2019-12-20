import os
import shutil
import json
import tarfile
import warnings
import logging
import io
warnings.filterwarnings('ignore')

import flask
from spleeter.separator import Separator
import os
from flask import Flask, Response, send_file
app = Flask(__name__)
app.debug = True

@app.route('/ping', methods=['GET'])
def ping():
    """
    Determine if the container is healthy by running a sample through the algorithm.
    """
    # we will return status ok if the model doesn't barf
    # but you can also insert slightly more sophisticated tests here

    try:
        Separator('base_config.json')
        return Response(response='{"status": "ok"}', status=200, mimetype='application/json')
    except:
        return Response(response='{"status": "error"}', status=500, mimetype='application/json')


@app.route('/invocations', methods=['POST'])
def seperate():
    try:
        Separator('base_config.json').separate_to_file('audio_example.mp3', 'output', synchronous=False)

        file_like_object = io.BytesIO()
        tar = tarfile.open(fileobj=file_like_object, mode='w|')
        for name in ["/Users/josh.prewer/Projects/spleeter/api/output/audio_example/vocals.wav", "/Users/josh.prewer/Projects/spleeter/api/output/audio_example/piano.wav"]:
            tar.add(name, os.path.basename(name))

        return send_file(file_like_object, attachment_filename='response.tar', mimetype='application/x-tar')
    except Exception as e:
        logging.exception(e)
        return Response(response='{"status": "error"}', status=500, mimetype='application/json')

