import os
import shutil
import json

import flask
import spleeter
from flask import Flask, Response
app = Flask(__name__)

# prefix = '/opt/ml'

# model_path = os.path.join(prefix, 'model')

# MODEL_NAME = os.environ.get("MODEL_FILENAME", "spleeter")

# class SeperationService(object):
    # model = None
    # data = None

    # @classmethod
    # def get_model(cls):
    #     """Get the model object for this instance, loading it if it's not already loaded."""
    #     if cls.model == None:
    #         cls.model = spleeter.separator.g
    #         cls.model.load(MODEL_NAME)
    #     return cls.model

@app.route('/ping', methods=['GET'])
def ping():
    """
    Determine if the container is healthy by running a sample through the algorithm.
    """
    # we will return status ok if the model doesn't barf
    # but you can also insert slightly more sophisticated tests here
    try:
        return Response(response='{"status": "ok"}', status=200, mimetype='application/json')
    except:
        return Response(response='{"status": "error"}', status=500, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def seperate():
    try:
        os.system('spleeter seperate -i audio_example.mp3 -o audio_output -p spleeter:5stems')
        return Response(response='{"status": "ok"}', status=200, mimetype='application/json')
    except:
        return Response(response='{"status": "error"}', status=500, mimetype='application/json')
