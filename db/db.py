from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.dialects import mysql

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    app.app_context().push()
    if not database_exists(db.engine.url):
        create_database(db.engine.url)
        db.create_all()


class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(mysql.LONGBLOB)
    hash = db.Column(mysql.BIGINT(unsigned=True))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

