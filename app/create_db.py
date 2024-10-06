from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime,timezone

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    predictions = db.relationship('Prediction', backref='user', lazy=True)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mean_radius = db.Column(db.Integer, nullable=False)
    mean_texture=db.Column(db.Integer, nullable=False)
    mean_perimeter=db.Column(db.Integer, nullable=False)
    mean_area=db.Column(db.Integer, nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default= datetime.now(timezone.utc))
