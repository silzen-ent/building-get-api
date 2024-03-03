# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
# Create a view that returns an array of all the games in our DB in JSON format whenever a GET request is made to /games 
@app.route('/games')
def games():

    # games = []
    # for game in Game.query.all():
    #     game_dict = game.to_dict()
        # {
        #     "title": game.title,
        #     "genre": game.genre,
        #     "platform": game.platform,
        #     "price": game.price,
        # }
        # games.append(game_dict)
    
    games = [game.to_dict() for game in Game.query.all()] # Create a list comprehension to make the above code more concise & succinct 

    response = make_response(
        # jsonify(games),
        games,
        200,
        # {"Content-Type": "application/json"}
    )

    return response

# Update app.py to add an additional view to get the game by id:
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    game_dict = game.to_dict()
    # {
    #     "title": game.title,
    #     "genre": game.genre,
    #     "platform": game.platform,
    #     "price": game.price,
    # }

    response = make_response(
        game_dict,
        200
    )

    return response


# Create a view that returns just the user data for a given game
@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    # users = []
    # for review in game.reviews:
    #     user = review.user
    #     user_dict = user.to_dict(rules=("-reviews",)) # We're excluding the reviews from each user by passing a rule into the to_dict method
    #     users.append(user_dict)

    # users = [review.user.to_dict(rules=('-reviews',))
    #          for review in game.reviews]

    # use association proxy to get users for a game
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    response = make_response(
        users,
        200
    )

    response = make_response(
        users,
        200
    )

    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)

