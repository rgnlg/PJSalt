from dota_team import app, db
from passlib.hash import sha256_crypt

from flask import render_template, url_for, redirect
from flask import flash, request
from flask_login import login_user, logout_user, current_user

from dota_team.forms import RegisterForm, LoginForm, TeamSearchForm
from dota_team.models import User


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm(request.form)
    if form.validate_on_submit():

        # create user registration object
        password_hash = sha256_crypt.encrypt(str(form.password.data))

        user = User(
            login=form.login.data,
            steam_login=form.login.data,
            password_hash=password_hash,
            mmr=form.mmr.data,
            aim=form.aim.data,
            position=form.position.data,
            server=form.server.data
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Successfully registered user {user.login}. Now you can login!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        valid_password = sha256_crypt.verify(form.password.data, user.password_hash)
        if user and valid_password:
            login_user(user)
            flash(f"Successfully logged in", "success")
            return redirect(url_for("profile"))
        
        flash("No such user! Please check username and password.", "danger")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/search', methods=["GET", "POST"])
def search():
    form = TeamSearchForm(request.form)

    # return render_template("search.html", query=query_position, user_data=users)
    return render_template("search.html", form=form)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template("profile.html")
