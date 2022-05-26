from flask_restful import Resource, fields, reqparse
from .validation import NotFoundError
from flask import current_app as app, jsonify
from app.db import db, User, Deck


class DeckScoreAPI(Resource):
    def get(self, deck_id):

        deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()

        if deck is None:
            raise NotFoundError(status_code=404)

        card_completed = [
            card.response for card in deck.deckcards if card.response != 0]

        score = int((sum(card_completed) / (len(deck.deckcards) * 3)
                     * 100) if len(deck.deckcards) else 0)

        return jsonify(deck_id=deck_id, score=score)


class UserScoreAPI(Resource):
    def get(self, user_id):

        user = db.session.query(User).filter_by(id=user_id).first()

        if user is None:
            raise NotFoundError(status_code=404)

        total_score = []

        for deck in user.userdeck:
            total_score.extend([card.response for card in deck.deckcards])

        len_total_score = len(total_score) if total_score else 0

        easy_score = total_score.count(3)
        easy = (int((easy_score * 3 / len_total_score) * 100)
                ) if len_total_score else 0

        medium_score = total_score.count(2)
        medium = (int((medium_score * 2 / len_total_score) * 100)
                  ) if len_total_score else 0

        hard_score = total_score.count(1)
        hard = (int((hard_score / len_total_score) * 100)) if len_total_score else 0

        total_score = (easy + medium + hard)

        return jsonify(id=user_id, total_score=total_score)
