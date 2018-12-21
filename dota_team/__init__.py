import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "dota_better_than_lol"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'main.db')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# migrate = Migrate(app, db)

from dota_team import routes, models


# creating main db if not exists
if not os.path.isfile(os.path.join(basedir, "main.db")):
    print("* Creating main db!")
    db.create_all()
