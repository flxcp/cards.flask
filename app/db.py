import os
import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db_path = f'sqlite:////{os.path.abspath("db/base.sqlite3")}'

Base = declarative_base()
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    userdeck = db.relationship('Deck', cascade="all, delete")


class Deck(db.Model):
    __tablename__ = 'deck'
    deck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, db.ForeignKey(
        'user.username'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.now())
    deckcards = db.relationship('Cards', cascade="all, delete")


class Cards(db.Model):
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey(
        'deck.deck_id'), nullable=False)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    response = db.Column(db.Integer, nullable=False, default=0)
