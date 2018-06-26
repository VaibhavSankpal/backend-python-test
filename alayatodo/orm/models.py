from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))

class Todos(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer)

    