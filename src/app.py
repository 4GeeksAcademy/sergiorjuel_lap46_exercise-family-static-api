"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Inicializar la familia Jackson
jackson_family = FamilyStructure("Jackson")

# Manejo de errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/members', methods=['POST'])
def add_member():
    member = request.get_json()
    if not member:
        return jsonify({"msg": "Invalid input"}), 400

    jackson_family.add_member(member)
    return jsonify(member), 200 


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "Member not found"}), 404
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
