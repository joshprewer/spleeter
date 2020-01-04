import os
import shutil
import json
import tarfile
import zipfile
import warnings
import logging
import io
warnings.filterwarnings('ignore')

import starlette
from spleeter.separator import Separator
from spleeter.audio.adapter import get_default_audio_adapter
from scipy.io.wavfile import write
import os

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response

app = Starlette(debug=True)
app.mount('/Users/josh.prewer/Projects/spleeter/api', StaticFiles(directory='/Users/josh.prewer/Projects/spleeter/api'), name='api')

@app.route('/ping')
async def ping(request):
    """
    Determine if the container is healthy by running a sample through the algorithm.
    """
    # we will return status ok if the model doesn't barf
    # but you can also insert slightly more sophisticated tests here

    try:
        Separator('/Users/josh.prewer/Projects/spleeter/api/base_config.json')
        return Response(status_code=200)
    except:
        return Response(status_code=500)


# @app.route('/invocations', methods=['POST'])
# def invocations():
#     try:
#         spearate()

#         return send_file(spearate(), attachment_filename='response.tar', mimetype='application/x-tar', as_attachment=True)
#     except Exception as e:
#         logging.exception(e)
#         return Response(response='{"status": "error"}', status=500, mimetype='application/json')


# def spearate():
#     separator = Separator('base_config.json')

#     audio_loader = get_default_audio_adapter()
#     sample_rate = 44100
#     waveform, _ = audio_loader.load('audio_example.mp3', sample_rate=sample_rate)

#     # Perform the separation :
#     prediction = separator.separate(waveform)

#     memory_object = io.BytesIO()
#     with tarfile.TarFile(memory_object, 'w') as tf:
#         for key in prediction:
#             wav = write(rate=44100, data=prediction[key])


#     print('tar completer')
#     return tar

