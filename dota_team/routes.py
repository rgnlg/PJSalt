from flask import render_template, url_for, redirect
from flask import flash, request, session

from dota_team.forms import  RegisterForm, LoginForm, TeamSearchForm

from dota_team import app

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    # TODO: Добавить возможность регистрации + редирект + сессию юзера + убрать регистр и логин на логаут и профайл

    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Registered user {form.login.data}(steam_login: {form.steam_login.data}) with aim {form.aim.data} from {form.server.data} server", "success")

    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash(f"Login request for user {form.login.data} with password {form.password.data}", "success")

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    return redirect(url_for("home"))

@app.route('/search', methods=["GET", "POST"])
def search():
    form = TeamSearchForm()

    # return render_template("search.html", query=query_position, user_data=users)
    return render_template("search.html", form=form)

@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template("profile.html")
