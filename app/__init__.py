from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
app = Flask(__name__)
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
         'id': os.environ['facebook_app_id'],
         'secret': os.environ['facebook_app_secret']
    }
}

if 'PRODUCTION' in os.environ:
    print("Running production config")
    app.config.from_object('secret_config')
else:
    print("Running test config")
    app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager(app)

from app import views
