from flask_restful import Resource, fields, marshal_with, reqparse
from .validation import NotFoundError
from flask import current_app as app
from app.db import db, Cards, Deck
import datetime

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('response')

response_fields = {
    "card_id": fields.Integer,
    "deck_id": fields.Integer,
    "question": fields.String,
    "answer": fields.String,
    "response": fields.Integer
}


class ResponseAPI(Resource):
    @marshal_with(response_fields)
    def put(self, card_id, response):

        card = db.session.query(Cards).filter_by(card_id=card_id).first()

        if card is None:
            raise NotFoundError(status_code=404)

        card.response = response

        db.session.add(card)
        db.session.commit()

        status = db.session.query(Cards).filter(
            (Cards.deck_id == card.deck_id) & (Cards.response == 0)).first()

        if status is None:
            deck = db.session.query(Deck).filter_by(
                deck_id=card.deck_id).first()
            deck.status = 1
            deck.date = datetime.datetime.now()

            db.session.add(deck)
            db.session.commit()
        else:
            deck = db.session.query(Deck).filter_by(
                deck_id=card.deck_id).first()
            deck.date = datetime.datetime.now()

            db.session.add(deck)
            db.session.commit()

        return card