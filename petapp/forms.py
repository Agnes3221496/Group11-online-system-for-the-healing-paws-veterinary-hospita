from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileRequired, FileAllowed
from flask_babel import Babel,lazy_gettext

# Customer Login
class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Remember Me'))
    submit = SubmitField(lazy_gettext('Sign In'))


# Employee Login
class EmployeeLoginForm(FlaskForm):
    employee_number = IntegerField(lazy_gettext('Employee&nbspNumber'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Remember Me'))
    submit = SubmitField(lazy_gettext('Sign In'))


# Customer Sign up
class SignupForm(FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    email = StringField(lazy_gettext('Email'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    password2 = PasswordField(lazy_gettext('Repeat Password'), validators=[DataRequired()])
    accept_rules = BooleanField(lazy_gettext('I accept the site rules'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Register'))


# Employee Sign up
class EmployeeSignupForm(FlaskForm):
    employee_number = StringField(lazy_gettext('Employee&nbspNumber'), validators=[DataRequired()])
    email = StringField(lazy_gettext('Email'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    password2 = PasswordField(lazy_gettext('Repeat Password'), validators=[DataRequired()])
    register_password = PasswordField(lazy_gettext('Register Password'), validators=[DataRequired()])
    accept_rules = BooleanField(lazy_gettext('I accept the site rules'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Register'))


class CatAppointmentForm(FlaskForm):
    name = StringField(lazy_gettext('Real Name: '), validators=[DataRequired()])
    phone = StringField(lazy_gettext('Phone Number: '), validators=[DataRequired()])
    city = RadioField(lazy_gettext('City'), choices=[(lazy_gettext('Beijing'), 'Beijing'), (lazy_gettext('Shanghai'), 'Shanghai'), (lazy_gettext('chengdu'), 'Chengdu')],
                      validators=[DataRequired()])
    pet = StringField(lazy_gettext('Please choose an existed pet '), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('book'))


# Customer post question
class PostQuestionForm(FlaskForm):
    title = StringField(lazy_gettext('Title'), validators=[DataRequired()])
    detail = StringField(lazy_gettext('Detail Description of The Question'), validators=[DataRequired()])
    image = FileField(lazy_gettext('Image'))
    submit = SubmitField(lazy_gettext('Post'))


# Customer search question
class SearchQuestionForm(FlaskForm):
    search = StringField(lazy_gettext('Question'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Search'))


class PostAnswerForm(FlaskForm):
    postbody = TextAreaField(lazy_gettext('Post body:'), validators=[DataRequired(lazy_gettext("Enter your post body"))])
    submit = SubmitField(lazy_gettext('Post answer'))


class PetForm(FlaskForm):
    name = StringField(lazy_gettext('Pet Name: '), validators=[DataRequired()])
    age = IntegerField(lazy_gettext('Age: '), validators=[DataRequired()])
    species = RadioField(lazy_gettext('Species'), choices=[(lazy_gettext('Cat'), 'Cat'), (lazy_gettext('Dog'), 'Dog')],
                         validators=[DataRequired()])
    image = FileField(lazy_gettext('Image'))
    submit = SubmitField(lazy_gettext('Submit'))

class LanguageForm(FlaskForm):
    language = SelectField(lazy_gettext('Language'), choices=[('en', 'English'), ('zh','简体中文')], validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Translate'))