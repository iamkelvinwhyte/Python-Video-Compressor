from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS, cross_origin

db = SQLAlchemy()
ma = Marshmallow()
 
def create_app(config_filename):
# set the project root directory as the static folder, you can set others.
    app = Flask(__name__,static_url_path='')
    CORS(app)
    app.config.from_object(config_filename)
   
    
    from app.auth import app_service
    #from app.chat import chat_service
    app.register_blueprint(app_service, url_prefix='/api')

  

    db.init_app(app)

    return app