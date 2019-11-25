from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/actors'

mongo = PyMongo(app)


@app.route('/actors', methods=['GET'])
def get_all_actors():
    actors = mongo.db.actors

    output = []

    for q in actors.find():
        output.append({'firstname': q['firstname'], 'lastname': q['lastname']})

    return jsonify(output)


@app.route('/actors/<_id>', methods=['GET'])
def get_id_actors(_id):
    actors = mongo.db.actors

    q = actors.find_one({'_id': ObjectId(_id)})

    output = []

    if q:
        for movie_name in q['movies']:
            output.append({'firstname': q['firstname'], 'lastname': q['lastname'], 'movie_name': movie_name})

    else:
        output = 'No actor found'

    return jsonify(output)


@app.route('/actors/name', methods=['GET'])
def get_firstname_actors():
    actors = mongo.db.actors
    firstname = request.args.get("firstname")

    output = []

    for q in actors.find({'firstname': firstname}):
        output.append({'firstname': q['firstname'], 'lastname': q['lastname']})

    return jsonify(output)


@app.route('/actors', methods=['POST'])
def add_actors():
    actors = mongo.db.actors

    firstname = request.json['firstname']
    lastname = request.json['lastname']

    movies = request.json['movies']

    actor_id = actors.insert({'firstname': firstname, 'lastname': lastname, 'movies': movies})
    new_actor = actors.find_one({'_id': actor_id})

    output = {'firstname': new_actor['firstname'], 'lastname': new_actor['lastname'], 'movies': new_actor['movies']}

    return jsonify({'result': output})


@app.route('/actors/movie/<movie_name>', methods=['GET'])
def get_actors_movie(movie_name):
    actors = mongo.db.actors

    output = []

    for q in actors.find({'movies': {"name": movie_name}}):
        output.append({'firstname': q['firstname'], 'lastname': q['lastname']})

    return jsonify(output)


@app.route("/actors/<_id>", methods=["PUT"])
def update_actor(_id):

    actors = mongo.db.actors
    q = actors.find_one({'_id': ObjectId(_id)})

    try:
        firstname = request.json['firstname']
    except KeyError as e:
        firstname = q['firstname']

    try:
        lastname = request.json['lastname']
    except KeyError as e:
        lastname = q['lastname']

    new_values = {"$set": {"firstname": firstname, "lastname": lastname}}
    actors.update_one(q, new_values)

    return "Actor" + '' + firstname + '' + "updated"

@app.route("/actors/<_id>", methods=["DELETE"])
def delete_actor(_id):

    actors = mongo.db.actors
    actors.delete_one({'_id': ObjectId(_id)})

    return "Actor" + ' ' + _id + ' ' + "deleted"


if __name__ == '__main__':
    app.run(debug=True)
