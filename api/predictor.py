import os
import shutil
import json
import warnings
warnings.filterwarnings('ignore')

import flask
from spleeter.separator import Separator
from flask import Flask, Response
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
        return Response(response='{"status": "ok"}', status=200, mimetype='application/json')
    except:
        return Response(response='{"status": "error"}', status=500, mimetype='application/json')