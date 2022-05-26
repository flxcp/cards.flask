from flask import render_template, redirect, url_for
from flask import current_app as app
from flask_login import login_required, current_user
from .db import db, User, Deck

@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', e=e), 404


@app.route("/", methods=["GET"])
@login_required
def dashboard():
    user = db.session.query(User).filter_by(
        username=current_user.username).first()

    incomplete_decks = []
    total_score = []

    for deck in user.userdeck:

        if deck.status == 0:
            card_completed = [
                card.response for card in deck.deckcards if card.response != 0]

            score = int((sum(card_completed) / (len(deck.deckcards) * 3)
                        * 100) if (len(deck.deckcards) != 0) else 0)

            total_score.extend([card.response for card in deck.deckcards])

            incomplete_decks.append((deck.deck_id, deck.name, len(
                card_completed), len(deck.deckcards), score))
        else:
            total_score.extend([card.response for card in deck.deckcards])

    len_total_score = len(total_score) if total_score else 0

    easy_score = total_score.count(3)
    easy = (int((easy_score * 3 / len_total_score) * 100)) if len_total_score else 0

    medium_score = total_score.count(2)
    medium = (int((medium_score * 2 / len_total_score) * 100)
              ) if len_total_score else 0

    hard_score = total_score.count(1)
    hard = (int((hard_score / len_total_score) * 100)) if len_total_score else 0

    base_score = sorted([easy, medium, hard])[1]

    easy_change = (int((easy / base_score) * 100)) if base_score else 0
    medium_change = (int((medium / base_score) * 100)) if base_score else 0
    hard_change = (int((hard / base_score) * 100)) if base_score else 0

    easy_change = (easy_change - medium_change)
    hard_change = (hard_change - medium_change)

    total_score = (easy + medium + hard)
    total_score_change = (total_score - 50)

    return render_template('dashboard.html', decks=incomplete_decks, easy_change=easy_change, medium_change=0, hard_change=hard_change, total_score_change=total_score_change, easy=easy, medium=medium, hard=hard, total_score=total_score)


@ app.route("/deck/<int:deck_id>/cards", methods=["GET"])
@ login_required
def cards(deck_id):

    deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()

    if deck is None:
        return render_template('404.html'), 404

    cards = [(card.card_id, card.question, card.answer, card.response)
             for card in deck.deckcards]

    return render_template('cards.html', cards=cards, deck_id=deck_id, deck_name=deck.name)


@ app.route("/deck", methods=["GET"])
@ login_required
def deck():
    user = db.session.query(User).filter_by(
        username=current_user.username).first()

    decks = []

    for deck in user.userdeck:

        card_completed = [
            card.response for card in deck.deckcards if card.response != 0]

        score = int((sum(card_completed) / (len(deck.deckcards) * 3)
                     * 100) if (len(deck.deckcards) != 0) else 0)

        decks.append((deck.deck_id, deck.name, deck.description, deck.status, len(deck.deckcards),
                      (f'{deck.date.day}.{deck.date.month}.{deck.date.year}'), score))

    return render_template('deck.html', decks=decks)


@ app.route("/review/deck/<int:deck_id>", methods=["GET"])
@ login_required
def review(deck_id):

    deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()

    if deck is None:
        return render_template('404.html'), 404

    cards = [(card.card_id, card.question, card.answer)
             for card in deck.deckcards if card.response == 0]

    card_start = (len(deck.deckcards) - (len(cards) - 1)) if (len(cards)
                                                              != 0) else (len(deck.deckcards))

    return render_template('review.html', cards=cards, deck_name=deck.name, card_start=card_start, card_end=len(deck.deckcards), deck_id=deck.deck_id)


@ app.route("/review/deck/<int:deck_id>/reset", methods=["GET"])
@ login_required
def reset_review(deck_id):
    deck = db.session.query(Deck).filter_by(deck_id=deck_id).first()

    if deck is None:
        return render_template('404.html'), 404

    deck.status = 0

    for card in deck.deckcards:
        card.response = 0

    db.session.add(deck)
    db.session.commit()

    return redirect(url_for('review', deck_id=deck_id))
