import os
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from facedetection import getBlendedImage
from flask.helpers import send_file

SAVE_FOLDER = "./img/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['SAVE_FOLDER'] = SAVE_FOLDER

if not os.path.exists('./img'):
    os.makedirs('./img')


@app.route("/")
def home():
    return "home"


@app.route("/file1", methods=['POST'])
def save_file1():
    if 'file' not in request.files:
        return Response(
            "NoFile",
            status=400,
        )
    file = request.files['file']
    if file.filename == '':
        return Response(
            "NoFileName",
            status=400,
        )
    if file and allowed_file(file.filename):
        print(file)
        filename = secure_filename(file.filename)
        fileExtention = filename.split('.')[1]
        file.save(os.path.join(
            app.config['SAVE_FOLDER'], "pic1." + fileExtention))
        return Response(
            "Done",
            status=200,
        )


@app.route("/file2", methods=['POST'])
def save_file2():
    if 'file' not in request.files:
        return Response(
            "NoFile",
            status=400,
        )
    file = request.files['file']
    if file.filename == '':
        return Response(
            "NoFileName",
            status=400,
        )
    if file and allowed_file(file.filename):
        print(file)
        filename = secure_filename(file.filename)
        fileExtention = filename.split('.')[1]
        file.save(os.path.join(
            app.config['SAVE_FOLDER'], "pic2." + fileExtention))
        return Response(
            "Done",
            status=200,
        )


@app.route("/blend", methods=['GET'])
def blending_images():
    getBlendedImage()
    try:
        return send_file('./merged/pic.png', attachment_filename='pic.png')
    except Exception as e:
        return str(e)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run()
