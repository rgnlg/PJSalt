from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "dota_better_than_lol"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dota_team/users.db"

db = SQLAlchemy(app)

from dota_team import routes