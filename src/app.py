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
from models import db, User, Score
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
def get_users():

    # obtiene todos los objetos de usuario de la base de datos
    users = User.query.all()

    # crea una lista de diccionarios con la información de cada usuario
    user_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email
            # agrega aquí cualquier otra información que quieras devolver
        }
        for user in users
    ]

    return jsonify(users), 200

@app.route('/score', methods=['GET'])
def get_scores():

    # obtiene todos los objetos de usuario de la base de datos
    scores = Score.query.all()

    # crea una lista de diccionarios con la información de cada usuario
    score_list = [
        {
            "machine": score.machine,
            "attempts": score.attempts,
            "elapsed_time": score.elapsed_time
            # agrega aquí cualquier otra información que quieras devolver
        }
        for score in scores
    ]

    return jsonify(score_list), 200

@app.route('/score', methods=['POST'])
def add_score():
    # get data from request
    data = request.get_json()

    # check if required fields are present
    if not all(key in data for key in ['machine', 'attempts', 'elapsed_time']):
        raise APIException('Missing fields', status_code=400)

    # validate attempts value
    if not 1 <= data['attempts'] <= 10:
        raise APIException('Invalid attempts value', status_code=400)

    # validate elapsed_time value
    if not 1 <= data['elapsed_time'] <= 60:
        raise APIException('Invalid elapsed_time value', status_code=400)

    # validate machine value
    if not isinstance(data['machine'], str) or len(data['machine']) > 80:
        raise APIException('Invalid machine value', status_code=400)

    # create new Score object
    score = Score(
        machine=data['machine'],
        attempts=data['attempts'],
        elapsed_time=data['elapsed_time']
    )

    # add score to database
    db.session.add(score)
    db.session.commit()

    return jsonify({'message': 'Score added successfully'}), 201


# this only runs if `$ python src/app.py` is executed 
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
