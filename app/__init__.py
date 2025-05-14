from flask import Flask
from flask_cors import CORS
from .auth import auth
from .routes import shopping

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)

    app.register_blueprint(auth)
    app.register_blueprint(shopping)

    return app
