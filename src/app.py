"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, Sernaggio has landed "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    response = request.get('https://swampi.dev/api/people/1')
    print(response)
    return response.json(), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    response = request.get('https://swampi.dev/api/planets/')
    print(response)
    return response.json(), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people():
    response = request.get('https://swapi.dev/api/people')
    print(response)
    return response.json(), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets():
    response = request.get('https://swapi.dev/api/planets')
    print(response)
    return response.json(), 200

@app.route('/users', methods=['GET'])
def get_users():
    response = request.get('https://swapi.dev/api/users')
    print(response)
    return response.json(), 200

@app.route('/users/favorites', methods=['GET'])
def get_planets():
    response = request.get('https://swapi.dev/api/favorites')
    print(response)
    return response.json(), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets():
    response = request.get('https://swapi.dev/api/planets')
    print(response)
    return response.json(), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets():
    response = request.get('https://swapi.dev/api/planets')
    print(response)
    return response.json(), 200

@app.route('/user/favorites/<int:user_id>', methods=['POST'])
def add_favorite_planet(user_id):
    user = User.query.get(user_id)  
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    planet_id = request.get_json()["planet_id"]
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'error': 'Planet not found'}), 404

    
    favorite = Favorite(user=user, planet=planet)
    db.session.add(favorite)
    db.session.commit()

    
    return jsonify({
        'user_id': user.id,
        'planet_id': planet.id
    }), 201

@app.route('/user/favorites/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite is None:
        return jsonify({'error': 'Favorite person not found for the user'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite person deleted successfully'})

@app.route('/user/favorites/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({'error': 'Favorite planet not found for the user'}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite planet deleted successfully'})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

