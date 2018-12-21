from dota_team import app, db
from passlib.hash import sha256_crypt

from flask import render_template, url_for, redirect
from flask import flash, request
from flask_login import login_user, logout_user, current_user

from dota_team.forms import RegisterForm, LoginForm, TeamSearchForm, UpdateProfileForm
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
            steam_login=form.steam_login.data,
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
        if not user:
            flash("No user with such login!", "danger")
            return redirect(url_for("login"))
        
        valid_password = sha256_crypt.verify(form.password.data, user.password_hash)
        if user and valid_password:
            login_user(user)
            flash(f"Successfully logged in", "success")
            return redirect(url_for("profile"))
        
        flash("No such user! Please check password.", "danger")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/search', methods=["GET", "POST"])
def search():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = TeamSearchForm(request.form)

    # return render_template("search.html", query=query_position, user_data=users)
    return render_template("search.html", form=form)


# TODO: добавить /profile/<str:user_login>
@app.route('/profile', methods=["GET", "POST"])
def profile():
    if current_user.is_authenticated:
        # костыль для дефолта в selectfiled
        form = UpdateProfileForm(
            login=current_user.login,
            steam_login=current_user.steam_login,
            mmr=current_user.mmr,
            aim=current_user.aim,
            position=current_user.position,
            server=current_user.server
        )
        if form.validate_on_submit():
            # хезе как выбрать только те, что изменены
            # vars() явно не подходит. данных мало так что апдейтим все!
            user = User.query.filter_by(login=current_user.login).update(dict(
                    login=form.login.data,
                    steam_login=form.steam_login.data,
                    mmr=form.mmr.data,
                    aim=form.aim.data,
                    position=form.position.data,
                    server=form.server.data
            ))
            db.session.commit()
            flash("Your profile info successfully updated!", "success")
            return redirect(url_for("profile"))
        return render_template("profile.html", form=form)
    else:
        flash("Your are not logged in yet!", "danger")
        return redirect(url_for("login"))


@app.route('/delete_profile')
def delete_profile():
    user = db.session.query(User).filter_by(login=current_user.login).first()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash("Your profile was deleted!", "danger")
    return redirect(url_for("login"))
