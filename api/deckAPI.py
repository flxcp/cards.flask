from flask_restful import Resource, fields, marshal_with, reqparse
from .validation import BusinessValidationError, NotFoundError
from flask import current_app as app
from app.db import db, Deck
from flask_login import current_user
from .cardAPI import response_fields as card_response_fields
import datetime

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('status')

response_fields = {
    "deck_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "status": fields.Integer,
    "date": fields.DateTime(dt_format='iso8601'),
    "deckcards": fields.List(fields.Nested(card_response_fields))
}


class DeckAPI(Resource):
    @marshal_with(response_fields)
    def get(self, deck_id):
        deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()
        if deck:
            return deck
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(response_fields)
    def post(self):
        args = parser.parse_args()
        username = (args.get('username', None) or current_user.username)
        name = args.get('name', None)
        description = args.get('description', None)
        status = (args.get('status', None) or 1)

        if username is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='DECK001',
                error_message='Username of Deck User is required')

        if name is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='DECK002',
                error_message='Deck Name is required')

        elif description is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='DECK003',
                error_message='Deck Description is required')

        deck = db.session.query(Deck).filter((Deck.username == username)
                                             & (Deck.name == name)).first()

        if deck:
            raise NotFoundError(status_code=409)

        deck = Deck(username=username,
                    name=name,
                    description=description,
                    status=status,
                    date=datetime.datetime.now())
        db.session.add(deck)
        db.session.commit()

        return deck, 201

    @marshal_with(response_fields)
    def put(self, deck_id):
        args = parser.parse_args()
        username = (args.get('username', None) or current_user.username)
        name = args.get('name', None)
        description = args.get('description', None)
        status = args.get('status', None)

        if username is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='DECK001',
                error_message='Username of Deck User is required')

        if name is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='DECK002',
                error_message='Deck Name is required')

        elif description is None:
            raise BusinessValidationError(
                status_code=400,
                error_code='DECK003',
                error_message='Deck Description is required')

        deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()

        if deck is None:
            raise NotFoundError(status_code=404)

        deck.username = username
        deck.name = name
        deck.description = description
        deck.date = datetime.datetime.now()

        if status:
            deck.status = status

        db.session.add(deck)
        db.session.commit()

        return deck

    def delete(self, deck_id):
        deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()

        if deck:
            db.session.delete(deck)
            db.session.commit()

            return '', 200

        if deck is None:
            raise NotFoundError(status_code=404)
