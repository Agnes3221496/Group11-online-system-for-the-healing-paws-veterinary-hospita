from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileRequired, FileAllowed
from flask_babel import Babel,lazy_gettext as _l, gettext as _
# from flask.ext.babel import lazy_gettext as _l

# Customer Login
class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


# Employee Login
class EmployeeLoginForm(FlaskForm):
    employee_number = IntegerField(_l('Employee&nbspNumber'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


# Customer Sign up
class SignupForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired()])
    accept_rules = BooleanField(_l('I accept the site rules'), validators=[DataRequired()])
    submit = SubmitField(_l('Register'))


# Employee Sign up
class EmployeeSignupForm(FlaskForm):
    employee_number = StringField(_l('Employee&nbspNumber'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired()])
    register_password = PasswordField(_l('Register Password'), validators=[DataRequired()])
    accept_rules = BooleanField(_l('I accept the site rules'), validators=[DataRequired()])
    submit = SubmitField(_l('Register'))


class CatAppointmentForm(FlaskForm):
    name = StringField(_l('Real Name: '), validators=[DataRequired()])
    phone = StringField(_l('Phone Number: '), validators=[DataRequired()])
    city = RadioField(_l('City'), choices=[(_l('Beijing'), 'Beijing'), (_l('Shanghai'), 'Shanghai'), (_l('chengdu'), 'Chengdu')],
                      validators=[DataRequired()])
    pet = StringField(_l('Please choose an existed pet '), validators=[DataRequired()])
    submit = SubmitField(_l('book'))


# Customer post question
class PostQuestionForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    detail = StringField(_l('Detail Description of The Question'), validators=[DataRequired()])
    image = FileField(_l('Image'))
    submit = SubmitField(_l('Post'))


# Customer search question
class SearchQuestionForm(FlaskForm):
    search = StringField(_l('Question'), validators=[DataRequired()])
    submit = SubmitField(_l('Search'))


class PostAnswerForm(FlaskForm):
    postbody = TextAreaField(_l('Post body:'), validators=[DataRequired(_l("Enter your post body"))])
    submit = SubmitField(_l('Post answer'))


class PetForm(FlaskForm):
    name = StringField(_l('Pet Name: '), validators=[DataRequired()])
    age = IntegerField(_l('Age: '), validators=[DataRequired()])
    species = RadioField(_l('Species'), choices=[(_l('Cat'), 'Cat'), (_l('Dog'), 'Dog')],
                         validators=[DataRequired()])
    image = FileField(_l('Image'))
    submit = SubmitField(_l('Submit'))

class HandleForm(FlaskForm):
    name = StringField(_l('Employee Number: '), validators=[DataRequired()])
    date = StringField(_l('Appointment date: '), validators=[DataRequired()])
    confirm = BooleanField(_l('Confirm handle this appointment'), validators=[DataRequired(_l('You need to confirm'))])
    submit = SubmitField(_l('Submit'))


class EmailCaptcha(FlaskForm):
    verificationCode = StringField("Enter the verification code please", validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))