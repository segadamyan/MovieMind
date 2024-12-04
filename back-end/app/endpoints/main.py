from flask import request, jsonify
from flask_restful import Resource
from app.chatbot import MovieChatbot
from app import app
from app.datasource import MovieDatasource

from app import api


class ChatBot(Resource):
    MOVIE_DATASOURCE = MovieDatasource(api_key=app.config.get("MOVIE_API_KEY"))
    MOVIE_DATASOURCE.update_movies(pages=1)
    BOT = MovieChatbot(openai_key=app.config.get("OPENAI_API_KEY"), movie_datasource=MOVIE_DATASOURCE)
    def get(self):
        return jsonify({"message": "Hello, World!"})
    
    def post(self):
        data = request.get_json()
        response, search_result = ChatBot.BOT.chat(data.get("input"))
        return jsonify({"message": response})

api.add_resource(ChatBot, "/chatbot")