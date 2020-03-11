from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, IntegerField
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
    city = RadioField('City', choices=[('0', 'Beijing'), ('1', 'Shanghai'), ('2', 'Chengdu')], validators=[DataRequired()])
    submit = SubmitField('book')
