from operator import and_

from werkzeug.utils import secure_filename

from petapp import app, db
from petapp.forms import LoginForm, EmployeeLoginForm, SignupForm, EmployeeSignupForm, CatAppointmentForm, \
    PostQuestionForm, SearchQuestionForm, PostAnswerForm, PetForm
from petapp.models import Customer, Employee, CatAppointment, DogAppointment, CatEmergency, DogEmergency, Question, \
    Answer, Pet

from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import time
from petapp.config import Config
import os
import re
import base64
import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = Customer.query.filter(Customer.username == form.username.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.username.data))
            return redirect(url_for('login'))
        if check_password_hash(user_in_db.password_hash, form.password.data):
            # flash('Login success!')
            session["USERNAME"] = user_in_db.username
            return redirect(url_for('standard_appointment_cat'))
        flash('Incorrect Password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    form = EmployeeLoginForm()
    if form.validate_on_submit():
        employee_in_db = Employee.query.filter(Employee.employee_number == form.employee_number.data).first()
        if not employee_in_db:
            flash('No user found with employee number: {}'.format(form.employee_number.data))
            return redirect(url_for('employee_login'))
        if check_password_hash(employee_in_db.password_hash, form.password.data):
            # flash('Login success!')
            session["NUMBER"] = employee_in_db.employee_number
            return redirect(url_for('orders'))
        flash('Incorrect Password')
        return redirect(url_for('employee_login'))
    return render_template('employee_login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))

        passw_hash = generate_password_hash(form.password.data)
        customer = Customer(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        db.session.add(customer)
        db.session.commit()
        # flash('User registered with username:{}'.format(form.username.data))
        session["USERNAME"] = customer.username
        return redirect(url_for("login"))
    return render_template('signup.html', title='Register a new user', form=form)


@app.route('/employee_signup', methods=['GET', 'POST'])
def employee_signup():
    form = EmployeeSignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('employee_signup'))
        if form.register_password.data != '123456':
            flash('Register password is not right!')
            return redirect(url_for('employee_signup'))

        passw_hash = generate_password_hash(form.password.data)
        employee = Employee(employee_number=form.employee_number.data, email=form.email.data, password_hash=passw_hash)
        db.session.add(employee)
        db.session.commit()
        # flash('User registered with username:{}'.format(form.username.data))
        session["NUMBER"] = employee.employee_number
        return redirect(url_for("employee_login"))
    return render_template('employee_signup.html', title='Register a new employee', form=form)


@app.route('/standard_appointment_cat', methods=['GET', 'POST'])
def standard_appointment_cat():
    form = CatAppointmentForm()
    # count = CatAppointment.query.count()
    b_count = CatAppointment.query.filter(CatAppointment.city == "Beijing").count()
    s_count = CatAppointment.query.filter(CatAppointment.city == "Shanghai").count()
    c_count = CatAppointment.query.filter(CatAppointment.city == "Chengdu").count()
    if form.validate_on_submit():
        if not session.get("USERNAME") is None:
            user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            catAppointment = CatAppointment(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                            customer_id=user_in_db.id)
            db.session.add(catAppointment)
            db.session.commit()
            return redirect(url_for("appointment_success"))
        else:
            flash("User needs to either login or signup first")
            return redirect(url_for('login'))

    return render_template('standard_appointment_cat.html', form=form, b_count=b_count, s_count=s_count,
                           c_count=c_count)


@app.route('/standard_appointment_dog', methods=['GET', 'POST'])
def standard_appointment_dog():
    form = CatAppointmentForm()
    # count = CatAppointment.query.count()
    b_count = DogAppointment.query.filter(DogAppointment.city == "Beijing").count()
    s_count = DogAppointment.query.filter(DogAppointment.city == "Shanghai").count()
    c_count = DogAppointment.query.filter(DogAppointment.city == "Chengdu").count()
    if form.validate_on_submit():
        if not session.get("USERNAME") is None:
            user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            dogAppointment = CatAppointment(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                            customer_id=user_in_db.id)
            db.session.add(dogAppointment)
            db.session.commit()
            return redirect(url_for("appointment_success"))
        else:
            flash("User needs to either login or signup first")
            return redirect(url_for('login'))

    return render_template('standard_appointment_dog.html', form=form, b_count=b_count, s_count=s_count,
                           c_count=c_count)


@app.route('/emergency_cat', methods=['GET', 'POST'])
def emergency_cat():
    form = CatAppointmentForm()
    # count = CatAppointment.query.count()
    if form.validate_on_submit():
        if not session.get("USERNAME") is None:
            user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            catEmergency = CatEmergency(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                        customer_id=user_in_db.id)
            db.session.add(catEmergency)
            db.session.commit()
            return redirect(url_for("appointment_success"))
        else:
            flash("User needs to either login or signup first")
            return redirect(url_for('login'))

    return render_template('emergency_cat.html', form=form)


@app.route('/emergency_dog', methods=['GET', 'POST'])
def emergency_dog():
    form = CatAppointmentForm()
    # count = CatAppointment.query.count()
    if form.validate_on_submit():
        if not session.get("USERNAME") is None:
            user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
            dogEmergency = DogEmergency(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                        customer_id=user_in_db.id)
            db.session.add(dogEmergency)
            db.session.commit()
            return redirect(url_for("appointment_success"))
        else:
            flash("User needs to either login or signup first")
            return redirect(url_for('login'))

    return render_template('emergency_dog.html', form=form)


@app.route('/appointment_success', methods=['GET', 'POST'])
def appointment_success():
    return render_template('appointment_success.html')


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('login'))


ALLOWED_FORMATS = ['png', 'jpg', 'gif', 'bmp', 'jfif']
@app.route('/post_question', methods=['GET', 'POST'])
def post_question():
    form = PostQuestionForm()
    if form.validate_on_submit():
        if not session.get("USERNAME") is None:
            image = request.files.get('image')
            suffix = image.filename.rsplit('.', image.filename.count('.'))[-1]
            if suffix.lower() in ALLOWED_FORMATS:
                filename = image.filename
                image_dir = Config.QUESTION_IMAGE_UPLOAD_DIR
                form.image.data.save(os.path.join(image_dir, filename))
                user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
                question = Question(publisher=user_in_db.id, title=form.title.data, detail=form.detail.data,
                                    image=filename, publish_date=datetime.datetime.now().replace(microsecond=0))
                db.session.add(question)
                db.session.commit()
                flash("Post successfully")
                return redirect(url_for('customer_question'))
            else:
                flash("The image format is wrong, please upload it again.")
                return redirect(url_for('post_question'))
        else:
            flash("User needs to either login or signup first")
            return redirect(url_for('login'))
    return render_template('post_question.html', title='Post Question', form=form)


@app.route('/customer_question', methods=['GET', 'POST'])
def customer_question():
    question = Question.query.all()
    form = SearchQuestionForm()
    if form.validate_on_submit():
        question = Question.query.filter(and_(Question.title.like("%" + form.search.data + "%"),
                                              Question.detail.like("%" + form.search.data + "%"))).all()
        return render_template('customer_question.html', title='Search', form=form, question=question)
    return render_template('customer_question.html', title='Search', form=form, question=question)

@app.route('/question_detail/<q_id>/')
def question_detail(q_id):
    question = Question.query.filter(Question.id == q_id)
    answer = Answer.query.filter(Answer.question_id == q_id)
    return render_template('question_detail.html', title='Detail', question=question, answer=answer)

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    return render_template('orders.html', title='Order List')


@app.route('/qa_e', methods=['GET', 'POST'])
def qa_e():
    prev_questions = Question.query.filter().all()
    return render_template('qa_e.html', title='Q&A', prev_questions=prev_questions)


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    form = PostAnswerForm()
    q = request.args.get("q")
    # print(q)
    prev_questions = Question.query.filter(Question.id == q).all()
    prev_answers = Answer.query.filter(Answer.question_id == q).all()
    if form.validate_on_submit():
        postbody = form.postbody.data
        employee_in_db = Employee.query.filter(Employee.employee_number == session.get("USERNAME")).first()
        dt = datetime.datetime.utcnow()
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour
        minutes = dt.minute
        time = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minutes)
        answer = Answer(answer=postbody, time=time, employee_id=employee_in_db.employee_number, question_id=q)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa_e'))
    return render_template('answer.html', title='Q&A', prev_questions=prev_questions, form=form, prev_answers=prev_answers)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        if not session.get("USERNAME") is None:
            image = request.files.get('image')
            suffix = image.filename.rsplit('.', image.filename.count('.'))[-1]
            if suffix.lower() in ALLOWED_FORMATS:
                filename = image.filename
                image_dir = Config.PET_IMAGE_UPLOAD_DIR
                form.image.data.save(os.path.join(image_dir, filename))
                user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
                pet = Pet(owner_id=user_in_db.id, name=form.name.data, age=form.age.data,
                                    image=filename, species=form.species.data)
                db.session.add(pet)
                db.session.commit()
                flash("Post successfully")
                return redirect(url_for('my_pets'))
            else:
                flash("The image format is wrong, please upload it again.")
                return redirect(url_for('add_pet'))
        else:
            flash("User needs to either login or signup first")
            return redirect(url_for('login'))
    return render_template('add_pet.html', title='Add Pet', form=form)

@app.route('/my_pets')
def my_pets():
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        pet = Pet.query.filter(Pet.owner_id == user_in_db.id)
        return render_template('my_pets.html', title='My Pets',pet=pet)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))
    return render_template('my_pets.html', title='My Pets',pet=pet)

@app.route('/pet_detail/<pet_id>/')
def pet_detail(pet_id):
    pet = Pet.query.filter(Pet.id == pet_id)
    return render_template('pet_detail.html', title='Detail', pet=pet)



