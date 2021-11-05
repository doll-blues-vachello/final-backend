from flask import Flask, request
from db.db import init_db, db
from db.db import ImageModel
# from resources.routes import init_routes
from os import environ
from PIL import Image
import sys
import socket
import time
import os
import signal
from io import BytesIO
from RnD.comparsion import dHash


def suicide(_, __):
    print("got term")
    os.kill(os.getpid(), signal.SIGINT)
signal.signal(signal.SIGTERM, suicide)


if 'DB_HOST' in environ.keys():
    db_host = environ['DB_HOST']
else:
    db_host = 'localhost'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:123@db/vezdekod'


init_db(app)

def find_similar(img: ImageModel)->list[ImageModel]:
    return db.session.query(ImageModel).from_statement(db.text("SELECT id FROM image_model where bit_count(hash ^ :chash) <= 3 AND ABS((width/height) - (:w/:h)) < 0.02")).params(chash=img.hash, w=img.width, h = img.height).all()



@app.post('/upload')
def upload():
    if 'file' not in request.files:
        return "No 'file' parameter", 400
    data = request.files['file'].stream
    try:
        img = Image.open(data)
        if img.format != 'JPEG':
            return "It must be a jpeg", 400
    except Exception as e:
        print(e)
        return "Bad image", 400
    data.seek(0)

    img = ImageModel(data=data.read(), width=img.width, height=img.height, hash=dHash(img))

    similars = find_similar(img)
    if len(similars) != 0:
        print("Found similar", file=sys.stderr)
        existing = similars[0]
        if existing.width < img.width:
            existing.width = img.width
            existing.height = img.height
            existing.data = img.data
            existing.hash = img.hash
            db.session.commit()
            print("Replaced", file=sys.stderr)
        return str(existing.id), 200

    db.session.add(img)
    db.session.commit()
    return str(img.id), 200


def scale_image(data: bytes, scale: float) -> bytes:
    file = BytesIO(data)
    img = Image.open(file)  # type: Image.Image
    img = img.resize((int(img.width * scale), int(img.height*scale)))
    file.truncate(0)
    file.seek(0)
    img.save(file, 'JPEG')
    file.seek(0)
    return file.read()


@app.get('/get')
def get():
    id = request.args.get('id')

    if id is None:
        return "Need id", 400
    try:
        id = int(id)
    except Exception:
        return "Invalid id", 400
    img = ImageModel.query.get(id)
    if img is None:
        return "Not found", 404

    data = img.data
    if 'scale' in request.args:
        scale = request.args.get('scale')
        try:
            scale = float(scale)
            data = scale_image(data, scale)
        except Exception as e :
            return "Invalid scale", 400
    # print(data)

    return data, 200, {'Content-Type': 'image/jpeg'}


if __name__ == '__main__':
    app.run(host='0.0.0.0')

# TODO: images