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
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    submit = SubmitField('Register')


class ProfileForm(FlaskForm):
    dob = DateField('Date of Birth (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('0', 'Male'), ('1', 'Female')], validators=[DataRequired()])
    cv = FileField('Your CV', validators=[FileAllowed(['pdf'], 'Only PDF files please')])
    submit = SubmitField('Update Profile')


class PostForm(FlaskForm):
    postbody = StringField('Text Draft', validators=[DataRequired()])
    receiver = RadioField('Receiver', choices=[('father', 'father'), ('mother', 'mother'), ('friends', 'friends')], validators=[DataRequired()])
    submit = SubmitField('Add Post')



class AddPhotoForm(FlaskForm):
    photo = FileField('', validators=[FileAllowed(['png'], 'Only PNG files please')])
    submit = SubmitField("Confirm")
