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
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from models import db, User, Planet, Character
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_characters():
    all_characters = db.session.execute(select(Character)).scalars().all()
    results = list(
        map(lambda character: character.serialize(), all_characters))
    return jsonify(results), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character_by_id(people_id):
    character = db.session.get(Character, people_id)
    if character is None:
        return jsonify({"msg": "Character not found"}), 404

    return jsonify(character.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = db.session.execute(select(Planet)).scalars().all()
    results = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(results), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = db.session.get(Planet, planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    results = list(map(lambda user: user.serialize(), users))
    return jsonify(results), 200






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
