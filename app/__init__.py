from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
app = Flask(__name__)
if 'PRODUCTION' in os.environ:
    print("Running production config")
    app.config.from_object('secret_config')
else:
    print("Running test config")
    app.config.from_object('config')

db = SQLAlchemy(app)

from app import views
