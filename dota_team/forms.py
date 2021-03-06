from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user

from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from dota_team.forms_choices import mmr_choices, position_choices, server_choices, aim_choices
from dota_team.forms_choices import mmr_choices_search, position_choices_search, aim_choices_search
from dota_team.models import User


class RegisterForm(FlaskForm):
    # TODO: добавить собственные сообщения об ошибках валидации - done
    login = StringField("Login", validators=[DataRequired(), Length(min=3, max=35)])
    steam_login = StringField("Steam Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=8, max=35), 
        EqualTo("second_password", message="Passwords do not match!"),
    ])
    second_password = PasswordField("Confirm Password")
    mmr = SelectField("MMR", choices=mmr_choices, coerce=str)
    position = SelectField("Position", choices=position_choices, coerce=str)
    server = SelectField("Server", choices=server_choices, coerce=str)
    aim = SelectField("Aim", choices=aim_choices, coerce=str)
    submit = SubmitField('Register Me')

    # raise error if login exists
    def validate_login(self, login):
        if User.query.filter_by(login=login.data).first():
            raise ValidationError("User with this login already exists, pick another one!")


class UpdateProfileForm(FlaskForm):
    login = StringField("Login", validators=[Length(min=3, max=35)])
    steam_login = StringField("Steam Login")
    profile_img = FileField("Profile logo", validators=[FileAllowed(["jpg", "png"])])
    mmr = SelectField("MMR", choices=mmr_choices, coerce=str)
    position = SelectField("Position", choices=position_choices, coerce=str)
    server = SelectField("Server", choices=server_choices, coerce=str)
    aim = SelectField("Aim", choices=aim_choices, coerce=str)
    submit = SubmitField('Update')

    # raise error if login exists
    def validate_login(self, login):
        if login.data != current_user.login:
            user = User.query.filter_by(login=login.data).first()
            if user:
                raise ValidationError("User with this login already exists, pick another one!")


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=3, max=35)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=35)])
    submit = SubmitField("Login")

    # def validate_login(self, login):
    #     user = User.query.filter_by(login=login.data).first()
    #     if not user:
    #         raise ValidationError("No such user!")


# пока что может быть оверкилл, но в будущем должна быть поисковая форма, а не просто запрос
class TeamSearchForm(FlaskForm):
    mmr = SelectField("MMR", choices=mmr_choices_search, coerce=str)
    position = SelectField("Position", choices=position_choices_search, coerce=str)
    aim = SelectField("Aim", choices=aim_choices_search, coerce=str)
    login_search = StringField("What are you looking for?")
    search = SubmitField("Search")
