from flask_socketio import  emit
from flask import request


from app.chatbot import MovieChatbot
from app import app, socketio
from app.datasource import MovieDatasource


MOVIE_DATASOURCE = MovieDatasource(api_key=app.config.get("MOVIE_API_KEY"))
BOT = MovieChatbot(openai_key=app.config.get("OPENAI_API_KEY"), movie_datasource=MOVIE_DATASOURCE)

chat_histories = {}

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    chat_histories[session_id] = []


@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in chat_histories:
        del chat_histories[session_id]


@socketio.on('user_input')
def handle_user_input(data):
    session_id = request.sid
    user_input = data.get('input')

    chat_histories[session_id].append({"user": user_input})

    response = BOT.chat_with_history(user_input, chat_histories[session_id])

    chat_histories[session_id].append({"bot": response})

    emit('message', {'message': response})

