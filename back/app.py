from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_methods": ["GET", "POST"]}})
client = MongoClient('localhost', 27017)

db = client.flask_database
campesinos_collection = db.campesinos_collection

@app.route("/create-new-campesino", methods=["POST"])
def create_new_campesino():
    data = request.get_json()

    require_fields = ["nombre", "edad", "cultivo", "experiencia", "origen"]
    if not all(field in data for field in require_fields):
        return jsonify({"error": "Missing required fields" }), 400

    new_campesino = {
        "nombre": data.get("nombre", "Joe Doe"),
        "edad": data.get("edad"),
        "cultivo": data.get("cultivo", "Tomates"),
        "origen": data.get("origen", "Desconocido"),
        "experiencia": data.get("experiencia", 0)
    }

    result = campesinos_collection.insert_one(new_campesino)
    new_campesino['_id'] = str(result.inserted_id)
    return jsonify(new_campesino), 201


@app.route("/get-campesinos", methods=["GET"])
def get_campesinos():
    all_campesinos = list(campesinos_collection.find({}, {"_id": 0}))
    return jsonify(all_campesinos)


@app.route("/get-campesinos-by-cultivo/<cultivo>", methods=["GET"])
def get_campesinos_by_cultivo(cultivo):
    campesinos = list(campesinos_collection.find({"cultivo": cultivo}, {"_id": 0}))
    return jsonify(campesinos)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)