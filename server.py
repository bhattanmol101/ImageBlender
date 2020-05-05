import os
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from facedetection import getBlendedImage
from flask.helpers import send_file
import logging
from datetime import datetime
from pytz import timezone
import shutil
import numpy as np

LOGGING_FILE = 'logs/app_server.log'

logging.basicConfig(
    filename=LOGGING_FILE,
    level=logging.INFO)
tz = timezone('Asia/Kolkata')
indiatime = datetime.now(tz)
logging.info(" " + indiatime.strftime('%Y-%m-%d %H:%M:%S') +
             ": application has started")

SAVE_FOLDER = "./img/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")


@app.route("/")
def home():
    return app.send_static_file("index.html")


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/count")
def counter():
    f = open('counter.in', 'r')
    count = int(f.read())
    f.close()
    count = count + 1
    f = open('counter.in', "w+")
    f.write(str(count))
    f.close()

    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')

    if os.path.exists('./merged'):
        shutil.rmtree('./merged')
    os.makedirs('./merged')
    indiatime = datetime.now(tz)
    logging.info(" " + indiatime.strftime('%Y-%m-%d %H:%M:%S') +
                 ": deleted old folders and created new folders")
    return "Done"


@app.route("/blend", methods=['POST'])
def blending_images():
    indiatime = datetime.now(tz)
    logging.info(
        " " + indiatime.strftime('%Y-%m-%d %H:%M:%S') + ": image blender called")
    try:
        images = request.files.getlist("file")
        indiatime = datetime.now(tz)
        logging.info(
            " " + indiatime.strftime('%Y-%m-%d %H:%M:%S') + ": both the images received")
        getBlendedImage(np.fromstring(images[0].read(), np.uint8), np.fromstring(
            images[1].read(), np.uint8))
        indiatime = datetime.now(tz)
        logging.info(
            " " + indiatime.strftime('%Y-%m-%d %H:%M:%S') + ": blended image sent")
        if os.path.exists('__pycache__'):
            shutil.rmtree('__pycache__')

        return send_file("./merged/pic.png", attachment_filename='pic.png')
    except Exception as e:
        indiatime = datetime.now(tz)
        logging.error(
            " " + indiatime.strftime('%Y-%m-%d %H:%M:%S') + ": error occurred while calling blendImage with error: " + e, e)
        return str(e)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(threaded=True)
