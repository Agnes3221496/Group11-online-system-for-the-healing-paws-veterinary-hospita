from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    IntegerField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileRequired, FileAllowed


# Customer Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Employee Login
class EmployeeLoginForm(FlaskForm):
    employee_number = IntegerField('Employee&nbspNumber', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Customer Sign up
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    submit = SubmitField('Register')


# Employee Sign up
class EmployeeSignupForm(FlaskForm):
    employee_number = StringField('Employee&nbspNumber', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    register_password = PasswordField('Register Password', validators=[DataRequired()])
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    submit = SubmitField('Register')


class CatAppointmentForm(FlaskForm):
    name = StringField('Real Name: ', validators=[DataRequired()])
    phone = StringField('Phone Number: ', validators=[DataRequired()])
    city = RadioField('City', choices=[('Beijing', 'Beijing'), ('Shanghai', 'Shanghai'), ('chengdu', 'Chengdu')],
                      validators=[DataRequired()])
    submit = SubmitField('book')


# Customer post question
class PostQuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    detail = StringField('Detail Description of The Question', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Post')


# Customer search question
class SearchQuestionForm(FlaskForm):
    search = StringField('Question', validators=[DataRequired()])
    submit = SubmitField('Search')


class PostAnswerForm(FlaskForm):
    postbody = TextAreaField('Post body:', validators=[DataRequired("Enter your post body")])
    submit = SubmitField('Post answer')
