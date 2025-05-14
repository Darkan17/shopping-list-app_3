from flask import current_app as app

def get_db():
    return app.config['MONGO_URI']