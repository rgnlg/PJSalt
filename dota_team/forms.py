from flask_wtf import FlaskForm

from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

from dota_team.forms_choices import mmr_choices, position_choices, server_choices, aim_choices


class RegisterForm(FlaskForm):
    # TODO: добавить собственные сообщения об ошибках валидации
    login = StringField("Login", validators=[DataRequired(), Length(min=3, max=35)])
    steam_login = StringField("Steam Login", validators=[DataRequired()])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=8, max=35), 
        EqualTo("second_password", message="Passwords do not match!"),
    ])
    second_password = PasswordField("Confirm Password")
    mmr = SelectField("MMR", choices=mmr_choices, coerce=str)
    position = SelectField("Position", choices=position_choices, coerce=int)
    server = SelectField("Server", choices=server_choices)
    aim = SelectField("Aim", choices=aim_choices, coerce=int)
    submit = SubmitField('Register Me')


class LoginForm(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=5, max=35)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=35)])
    submit = SubmitField("Login")


# пока что может быть оверкилл, но в будущем должна быть поисковая форма, а не просто запрос
class TeamSearchForm(FlaskForm):
    search_query = StringField("What are you looking for?")
    search = SubmitField("Search")
