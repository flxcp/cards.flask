from flask import Flask
from flask_restful import Api
from app.db import db, db_path
from flask_login import LoginManager
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'
db.init_app(app)


@app.before_first_request
def create_db():
    db.create_all()


# Flask Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
login_manager.login_message_category = "danger"

# Flask Logging
logging.basicConfig(filename='cards.log', level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(name)s in %(module)s: %(message)s')

# Flask API
api = Api(app)
app.app_context().push()

# Import all the controllers
from app.auth import *   # noqa
from app.controllers import *   # noqa

# Add all restful controllers
from api.deckAPI import DeckAPI   # noqa
from api.cardAPI import CardAPI   # noqa
from api.resApi import ResponseAPI   # noqa
from api.scoreAPI import DeckScoreAPI, UserScoreAPI   # noqa
api.add_resource(DeckAPI, "/api/deck", "/api/deck/<int:deck_id>")
api.add_resource(CardAPI, "/api/card", "/api/card/<int:card_id>")
api.add_resource(ResponseAPI, "/api/card/<int:card_id>/res/<int:response>")
api.add_resource(DeckScoreAPI, "/api/deck/<int:deck_id>/score")
api.add_resource(UserScoreAPI, "/api/user/<int:user_id>/score")

if __name__ == '__main__':
    app.run()
