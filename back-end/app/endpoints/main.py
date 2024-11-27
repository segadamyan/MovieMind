from flask import request, jsonify
from flask_restful import Resource

from app import api


class Movie(Resource):

    def get(self):
        return jsonify({"message": "Hello, World!"})
    
    def post(self):
        data = request.get_json()
        return jsonify(data)