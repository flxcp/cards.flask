from flask_restful import Resource, fields, marshal_with, reqparse
from .validation import BusinessValidationError, NotFoundError
from flask import current_app as app
from app.db import db, Cards, Deck

# Define Request Parser
parser = reqparse.RequestParser()
parser.add_argument('deck_id')
parser.add_argument('question')
parser.add_argument('answer')
parser.add_argument('response')

response_fields = {
    "card_id": fields.Integer,
    "deck_id": fields.Integer,
    "question": fields.String,
    "answer": fields.String,
    "response": fields.Integer
}


class CardAPI(Resource):
    @marshal_with(response_fields)
    def get(self, card_id):

        card = db.session.query(Cards).filter_by(card_id=card_id).first()

        if card:
            return card
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(response_fields)
    def post(self):
        args = parser.parse_args()
        deck_id = args.get('deck_id', None)
        question = args.get('question', None)
        answer = args.get('answer', None)
        response = (args.get('response', None) or 0)

        if deck_id is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD001', error_message='Deck User ID is required')

        elif question is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD002', error_message='Question is required')

        elif answer is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD003', error_message='Answer is required')

        card = db.session.query(Cards).filter((Cards.deck_id == deck_id) & (
            Cards.response == response) & (Cards.question == question)).first()

        if card:
            raise NotFoundError(status_code=409)

        card = Cards(deck_id=deck_id, question=question,
                     answer=answer, response=response)

        db.session.add(card)
        db.session.commit()

        deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()
        deck.status = 0

        db.session.add(deck)
        db.session.commit()

        return card, 201

    @marshal_with(response_fields)
    def put(self, card_id):
        args = parser.parse_args()
        deck_id = args.get('deck_id', None)
        question = args.get('question', None)
        answer = args.get('answer', None)
        response = (args.get('response', None) or 0)

        if deck_id is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD001', error_message='Deck User ID is required')

        elif question is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD002', error_message='Question is required')

        elif answer is None:
            raise BusinessValidationError(
                status_code=400, error_code='CARD003', error_message='Answer is required')

        card = db.session.query(Cards).filter_by(card_id=card_id).first()

        if card is None:
            raise NotFoundError(status_code=404)

        card.deck_id = deck_id
        card.question = question
        card.answer = answer
        card.response = response

        db.session.add(card)
        db.session.commit()

        deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()
        deck.status = 0

        db.session.add(deck)
        db.session.commit()

        return card

    def delete(self, card_id):
        card = db.session.query(Cards).filter_by(card_id=card_id).first()

        if card:
            db.session.delete(card)
            db.session.commit()

            return '', 200

        if card is None:
            raise NotFoundError(status_code=404)
