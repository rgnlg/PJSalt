from dota_team import app, db

from flask import render_template, url_for, redirect
from flask import flash, request, session

from dota_team.forms import RegisterForm, LoginForm, TeamSearchForm
from dota_team.models import User


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # create user registration object
        user = User(
            login=form.login.data,
            steam_login=form.login.data,
            password_hash=form.password.data,
            mmr=form.mmr.data,
            aim=form.aim.data,
            position=form.position.data,
            server=form.server.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Successfully registered user {user.login}. Now you can login!", "success")
        return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data

        flash(f"Login request for user {login} with password {password}", "success")

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    return redirect(url_for("home"))


@app.route('/search', methods=["GET", "POST"])
def search():
    form = TeamSearchForm(request.form)

    # return render_template("search.html", query=query_position, user_data=users)
    return render_template("search.html", form=form)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template("profile.html")
