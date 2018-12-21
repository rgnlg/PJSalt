from dota_team import db

# for errors with pylint use pylint-flask
# source: https://github.com/PyCQA/pylint/issues/1973
# of just change linter to flake8 :\


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(35), unique=True, nullable=False)
    steam_login = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    mmr = db.Column(db.String(5), nullable=False)
    aim = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    # in the future - many-to-many relation - separate db
    server = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.login}', '{self.server}')"


# class Requests(db.Model):
#     pass


# test_user = User(login="Howuhh", steam_login="Howuhh", password_hash="12345678", mrr=">6k", aim=1, postion=1, server="eu")