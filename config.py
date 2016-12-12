import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.environ['PG_user'] +':' + os.environ['PG_pass'] + '@localhost:5432/expense_tracker'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'expense_db_repo')
SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = True
SECRET_KEY = "babablacksheep"

