#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games', methods = [ 'GET', 'POST' ] )
def games():

    body = None
    status_code = None
    if request.method == 'GET' :
        games = []
        for game in Game.query.all():
            game_dict = {
                'id': game.id,
                "title": game.title,
                "genre": game.genre,
                "platform": game.platform,
                "price": game.price,
            }
            games.append(game_dict)
        body = jsonify( games )
        status_code = 200
    elif request.method == 'POST' :
        # print( request.get_json() )
        post_game = request.get_json()
        new_game = Game(
            genre = post_game['genre'],
            platform = post_game['platform'],
            title = post_game['title'],
            price = post_game['price'],
        )

        db.session.add( new_game )
        db.session.commit()
        
        body = jsonify( new_game.to_dict() )
        status_code = 201


    response = make_response(
        body,
        status_code
    )

    return response

@app.route('/games/<int:id>', methods = [ 'GET', 'DELETE', 'PATCH' ] )
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    body = None
    status_code = None
    if game :
        if request.method == 'GET' :
            game_dict = game.to_dict()
            body = jsonify( game_dict )
            status_code = 200
        elif request.method == 'DELETE' :
            db.session.delete( game )
            db.session.commit()
            body = {
                'delete_successful': True,
                'message': 'Review was deleted.'
            }
            status_code = 200
        elif request.method == 'PATCH' :
            for key in request.get_json() :
                setattr( game, key, request.get_json()[ key ] )
            
            db.session.add( game )
            db.session.commit()
            body = jsonify( game.to_dict() )
            status_code = 200
    else :
        body = 'Could not find game.'
        status_code = 404

    return make_response( body, status_code )

    

@app.route('/reviews')
def reviews():

    reviews = []
    for review in Review.query.all():
        review_dict = review.to_dict()
        reviews.append(review_dict)

    response = make_response(
        reviews,
        200
    )

    return response

@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
