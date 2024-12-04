import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from app.config import ProductionConfig, DevelopmentConfig
from flask_cors import CORS


CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, headers=[])

if os.environ["env"] == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)
    

app.secret_key = app.config.get("SECRET_KEY")


from app.endpoints import main
