import random
import string
from operator import and_

from flask_mail import Message
from werkzeug.utils import secure_filename

from petapp import app, db, mail
from petapp.forms import LoginForm, EmployeeLoginForm, SignupForm, EmployeeSignupForm, CatAppointmentForm, \
    PostQuestionForm, SearchQuestionForm, PostAnswerForm, PetForm, PostQuestionForm, SearchQuestionForm, PostAnswerForm, \
    PetForm, HandleForm, PostQuestionForm, SearchQuestionForm, PostAnswerForm, PetForm, PostQuestionForm, \
    SearchQuestionForm, PostAnswerForm, PetForm, HandleForm, EmailCaptcha
from petapp.models import Customer, Employee, CatAppointment, DogAppointment, CatEmergency, DogEmergency, Question, \
    Answer, Pet, HandleDetails

from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import time
from petapp.config import Config
import os
import re
import base64
import datetime
from petapp import babel
from flask_babel import Babel, format_date, gettext, lazy_gettext


# app.config['BABEL_DEFAULT_LOCALE'] = 'zh'

@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/language/<language>')
def choose_language(language=None):
    session['language'] = language
    if session.get("currentPage") == 'pet_detail':
        return redirect(url_for(session.get("currentPage"), pet=session.get('petID')))
    elif session.get("currentPage") == 'question_detail':
        return redirect(url_for(session.get("currentPage"), q=session.get('questionID')))
    else:
        return redirect(url_for(session.get("currentPage")))


@app.context_processor
def inject_conf_var():
    return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'],
                CURRENT_LANGUAGE=session.get('language',
                                             request.accept_languages.best_match(app.config['LANGUAGES'].keys())))


# @app.context_processor
# def inject_conf_var():
#     return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'],
#                 CURRENT_LANGUAGE=session.get('language',
#                                              request.accept_languages.best_match(app.config['LANGUAGES'].keys())))


# reference: https://www.thinbug.com/q/42393831

@app.route('/')
@app.route('/index')
def index():
    session['currentPage'] = 'index'
    session['currentPage'] = 'index'
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['currentPage'] = 'login'
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = Customer.query.filter(Customer.username == form.username.data).first()
        if not user_in_db:
            flash(gettext('No user found with username: %(name)s', name=form.username.data))
            flash(gettext('No user found with username: %(name)s', name=form.username.data))
            return redirect(url_for('login'))
        if check_password_hash(user_in_db.password_hash, form.password.data):
            # flash('Login success!')
            session["USERNAME"] = user_in_db.username
            return redirect(url_for('standard_appointment_cat'))
        flash(gettext('Incorrect Password'))
        return redirect(url_for('login'))
    return render_template('login.html', title=gettext('Sign In'), form=form)


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    session['currentPage'] = 'employee_login'
    form = EmployeeLoginForm()
    if form.validate_on_submit():
        employee_in_db = Employee.query.filter(Employee.employee_number == form.employee_number.data).first()
        if not employee_in_db:
            flash(gettext('No user found with employee number: {}'.format(form.employee_number.data)))
            return redirect(url_for('employee_login'))
        if check_password_hash(employee_in_db.password_hash, form.password.data):
            # flash('Login success!')
            session["NUMBER"] = employee_in_db.employee_number
            return redirect(url_for('orders'))
        flash(gettext('Incorrect Password'))
        return redirect(url_for('employee_login'))
    return render_template('employee_login.html', title=gettext('Sign In'), form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session['currentPage'] = 'signup'
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash(gettext('Passwords do not match!'))
            return redirect(url_for('signup'))
        passw_hash = generate_password_hash(form.password.data)
        global customer
        customer = Customer(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        # db.session.add(customer)
        # db.session.commit()
        # flash('User registered with username:{}'.format(form.username.data))
        # session["USERNAME"] = customer.username
        return redirect(url_for("email_captcha"))
    return render_template('signup.html', title=gettext('Register a new user'), form=form)


@app.route('/email_captcha', methods=['GET', 'POST'])
def email_captcha():
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))
    print(captcha)
    global Verification_code
    Verification_code = str(captcha)
    print(customer)
    message = Message(subject='Verification Code', sender="shenlingwudi@126.com", recipients=[customer.email], body=captcha)
    try:
        mail.send(message)
    except:
        flash("server error, unable to send verification message, please try again later")
        return redirect(url_for('login'))
    return redirect(url_for('email_verification'))


@app.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
    print(123)
    form = EmailCaptcha()
    if form.validate_on_submit():
        code = form.verificationCode.data
        print(code)
        if code != Verification_code:
            flash("The verification code is wrong, please check your email address and register agian")
            return redirect(url_for('signup'))
        if code == Verification_code:
            db.session.add(customer)
            db.session.commit()
            flash("registered successfully")
            return redirect(url_for('login'))
    return render_template('email_captcha.html', title=email_captcha, form=form)


@app.route('/checkuser', methods=['POST'])
def check_username():
    chosen_name = request.form['username']
    user_in_db = Customer.query.filter(Customer.username == chosen_name).first()
    if not user_in_db:
        return jsonify({'text': gettext('Username is available'),
                        'returnvalue': 0})
    else:
        return jsonify({'text': gettext('Sorry! Username is already taken'),
                        'returvalue': 1})


@app.route('/checkemail', methods=['POST'])
def check_email():
    chosen_email = request.form['email']
    user_in_db = Customer.query.filter(Customer.email == chosen_email).first()
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not user_in_db:
        if re.search(regex, chosen_email):
            return jsonify({'text': gettext('Email is available'), 'returnvalue': 2})
        else:
            return jsonify({'text': gettext('Incorrect format!'), 'returnvalue': 1})
    else:
        return jsonify({'text': gettext('Email is already existed'), 'returnvalue': 0})


@app.route('/employee_signup', methods=['GET', 'POST'])
def employee_signup():
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'employee_signup'
        form = EmployeeSignupForm()
        if form.validate_on_submit():
            if form.password.data != form.password2.data:
                flash(gettext('Passwords do not match!'))
                return redirect(url_for('employee_signup'))
            if form.register_password.data != '123456':
                flash(gettext('Register password is not right!'))
                return redirect(url_for('employee_signup'))

            passw_hash = generate_password_hash(form.password.data)
            employee = Employee(employee_number=form.employee_number.data, email=form.email.data,
                                password_hash=passw_hash)
            db.session.add(employee)
            db.session.commit()
            # flash('User registered with username:{}'.format(form.username.data))
            session["NUMBER"] = employee.employee_number
            return redirect(url_for("employee_login"))
        return render_template('employee_signup.html', title=gettext('Register a new employee'), form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


@app.route('/services')
def services():
    session['currentPage'] = 'services'
    return render_template('services.html')


@app.route('/about')
def about():
    session['currentPage'] = 'about'
    return render_template('about.html')


@app.route('/blog')
def blog():
    session['currentPage'] = 'blog'
    return render_template('blog.html')


@app.route('/gallery')
def gallery():
    session['currentPage'] = 'gallery'
    return render_template('gallery.html')


@app.route('/standard_appointment_cat', methods=['GET', 'POST'])
def standard_appointment_cat():
    session['currentPage'] = 'standard_appointment_cat'
    form = CatAppointmentForm()
    # count = CatAppointment.query.count()
    b_count = CatAppointment.query.filter(CatAppointment.city == "Beijing").count()
    s_count = CatAppointment.query.filter(CatAppointment.city == "Shanghai").count()
    c_count = CatAppointment.query.filter(CatAppointment.city == "Chengdu").count()

    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        cats = Pet.query.filter(and_(Pet.owner_id == user_in_db.id, Pet.species == "Cat")).all()
        cat_name = []
        for c in cats:
            cat_name.append(c.name)

        if form.validate_on_submit():
            if form.pet.data in cat_name:
                pet = Pet.query.filter(
                    and_(Pet.name == form.pet.data, and_(Pet.owner_id == user_in_db.id, Pet.species == "Cat"))).first()
                catAppointment = CatAppointment(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                                customer_id=user_in_db.id, pet_name=form.pet.data, pet_id=pet.id)
                db.session.add(catAppointment)
                db.session.commit()
                return redirect(url_for("appointment_success"))
            else:
                flash(gettext("Please add the pet first *^_^*"))
                return redirect(url_for('standard_appointment_cat'))

        else:
            return render_template('standard_appointment_cat.html', form=form, b_count=b_count, s_count=s_count,
                                   c_count=c_count, cats=cats)
    else:
        flash(gettext("User needs to either login or signup first"))
        return redirect(url_for('login'))


@app.route('/standard_appointment_dog', methods=['GET', 'POST'])
def standard_appointment_dog():
    session['currentPage'] = 'standard_appointment_dog'
    form = CatAppointmentForm()
    # count = CatAppointment.query.count()
    b_count = DogAppointment.query.filter(DogAppointment.city == "Beijing").count()
    s_count = DogAppointment.query.filter(DogAppointment.city == "Shanghai").count()
    c_count = DogAppointment.query.filter(DogAppointment.city == "Chengdu").count()

    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        dogs = Pet.query.filter(and_(Pet.owner_id == user_in_db.id, Pet.species == "Dog")).all()
        dog_name = []
        for d in dogs:
            dog_name.append(d.name)

        if form.validate_on_submit():
            if form.pet.data in dog_name:
                pet = Pet.query.filter(
                    and_(Pet.name == form.pet.data, and_(Pet.owner_id == user_in_db.id, Pet.species == "Dog"))).first()
                dogAppointment = DogAppointment(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                                customer_id=user_in_db.id, pet_name=form.pet.data, pet_id=pet.id)
                db.session.add(dogAppointment)
                db.session.commit()
                return redirect(url_for("appointment_success"))
            else:
                flash(gettext("Please add the pet first *^_^*"))
                return redirect(url_for('standard_appointment_dog'))
        else:
            return render_template('standard_appointment_dog.html', form=form, b_count=b_count, s_count=s_count,
                                   c_count=c_count, dogs=dogs)
    else:
        flash(gettext("User needs to either login or signup first"))
        return redirect(url_for('login'))


@app.route('/emergency_cat', methods=['GET', 'POST'])
def emergency_cat():
    session['currentPage'] = 'emergency_cat'
    form = CatAppointmentForm()

    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        cats = Pet.query.filter(and_(Pet.owner_id == user_in_db.id, Pet.species == "Cat")).all()
        cat_name = []
        for c in cats:
            cat_name.append(c.name)

        if form.validate_on_submit():
            if form.pet.data in cat_name:
                pet = Pet.query.filter(
                    and_(Pet.name == form.pet.data, and_(Pet.owner_id == user_in_db.id, Pet.species == "Cat"))).first()
                user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
                catEmergency = CatEmergency(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                            customer_id=user_in_db.id, pet_name=form.pet.data, pet_id=pet.id)
                db.session.add(catEmergency)
                db.session.commit()
                return redirect(url_for("appointment_success"))
            else:
                flash(gettext("Please add the pet first *^_^*"))
                return redirect(url_for('emergency_cat'))
        else:
            return render_template('emergency_cat.html', form=form, cats=cats)
    else:
        flash(gettext("User needs to either login or signup first"))
        return redirect(url_for('login'))


@app.route('/emergency_dog', methods=['GET', 'POST'])
def emergency_dog():
    session['currentPage'] = 'emergency_dog'
    form = CatAppointmentForm()

    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        dogs = Pet.query.filter(and_(Pet.owner_id == user_in_db.id, Pet.species == "Dog")).all()
        dog_name = []
        for d in dogs:
            dog_name.append(d.name)

        if form.validate_on_submit():
            if form.pet.data in dog_name:
                pet = Pet.query.filter(
                    and_(Pet.name == form.pet.data, and_(Pet.owner_id == user_in_db.id, Pet.species == "Dog"))).first()
                user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
                dogEmergency = DogEmergency(name=form.name.data, phone=form.phone.data, city=form.city.data,
                                            customer_id=user_in_db.id, pet_name=form.pet.data, pet_id=pet.id)
                db.session.add(dogEmergency)
                db.session.commit()
                return redirect(url_for("appointment_success"))
            else:
                flash(gettext("Please add the pet first *^_^*"))
                return redirect(url_for('emergency_dog'))
        else:
            return render_template('emergency_dog.html', form=form, dogs=dogs)
    else:
        flash(gettext("User needs to either login or signup first"))
        return redirect(url_for('login'))


@app.route('/appointment_success', methods=['GET', 'POST'])
def appointment_success():
    session['currentPage'] = 'appointment_success'
    return render_template('appointment_success.html')


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    session.pop("NUMBER", None)
    return redirect(url_for('login'))


ALLOWED_FORMATS = ['png', 'jpg', 'gif', 'bmp', 'jfif']


@app.route('/post_question', methods=['GET', 'POST'])
def post_question():
    session['currentPage'] = 'post_question'
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
                flash(gettext("Post successfully"))
                return redirect(url_for('customer_question'))
            else:
                flash(gettext("The image format is wrong, please upload it again."))
                return redirect(url_for('post_question'))
        else:
            flash(gettext("User needs to either login or signup first"))
            return redirect(url_for('login'))
    return render_template('post_question.html', title=gettext('Post Question'), form=form)


@app.route('/customer_question', methods=['GET', 'POST'])
def customer_question():
    session['currentPage'] = 'customer_question'
    question = Question.query.all()
    form = SearchQuestionForm()
    if form.validate_on_submit():
        question = Question.query.filter(and_(Question.title.like("%" + form.search.data + "%"),
                                              Question.detail.like("%" + form.search.data + "%"))).all()
        return render_template('customer_question.html', title=gettext('Search'), form=form, question=question)
    return render_template('customer_question.html', title=gettext('Search'), form=form, question=question)


@app.route('/question_detail', methods=['GET', 'POST'])
def question_detail():
    session['currentPage'] = 'question_detail'
    # session['questionID'] = q_id
    q = request.args.get("q")
    question = Question.query.filter(Question.id == q).all()
    print(question)
    answer = Answer.query.filter(Answer.question_id == q).all()
    print(answer)
    return render_template('question_detail.html', title=gettext('Detail'), question=question, answer=answer)


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'orders'
        cat_orders_e = CatEmergency.query.filter(CatEmergency.status == 0).all()
        dog_orders_e = DogEmergency.query.filter(DogEmergency.status == 0).all()
        cat_orders = CatAppointment.query.filter(CatAppointment.status == 0).all()
        dog_orders = DogAppointment.query.filter(DogAppointment.status == 0).all()

        user_in_db = Employee.query.filter(Employee.employee_number == session.get("NUMBER")).first()
        order_details = HandleDetails.query.filter(HandleDetails.employee_id == user_in_db.id).all()
        for orders in order_details:
            if orders.finish_date != 'Undetermined' and orders.finish_date != 'In treatment':
                dt = datetime.datetime.now() - datetime.timedelta(days=7)
                time = str(dt)
                time = time[:16]
                if orders.finish_date < time:
                    print(orders.appointment_id)
                    if orders.appointment_type == 1:
                        if orders.pet_type == 1:
                            ce = CatEmergency.query.filter(CatEmergency.id == orders.appointment_id).first()
                            db.session.delete(ce)
                            db.session.commit()
                        else:
                            cn = DogEmergency.query.filter(DogEmergency.id == orders.appointment_id).first()
                            db.session.delete(cn)
                            db.session.commit()
                    else:
                        if orders.pet_type == 1:
                            de = CatAppointment.query.filter(CatAppointment.id == orders.appointment_id).first()
                            db.session.delete(de)
                            db.session.commit()
                        else:
                            dn = DogAppointment.query.filter(DogAppointment.id == orders.appointment_id).first()
                            db.session.delete(dn)
                            db.session.commit()
                    db.session.delete(orders)
                    db.session.commit()
                    print('6657')

        return render_template('orders.html', title=gettext('Order List'), cat_orders_e=cat_orders_e,
                               dog_orders_e=dog_orders_e, cat_orders=cat_orders, dog_orders=dog_orders)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


@app.route('/handle_details', methods=['GET', 'POST'])
def handle_details():
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'handle_details'
        form = HandleForm()
        user_in_db = Employee.query.filter(Employee.employee_number == session.get("NUMBER")).first()
        c = request.args.get("c")
        ce = request.args.get("ce")
        d = request.args.get("d")
        de = request.args.get("de")
        pt = 1  # 1 is cat, 2 is dog
        at = 1  # 1 is emergency, 2 is normal
        aid = 0
        priority = 0
        if form.validate_on_submit():
            if c is not None:
                print("1")
                cat = CatAppointment.query.filter(CatAppointment.id == c).first()
                cat.status = user_in_db.id
                db.session.commit()
                pt = 1
                at = 2
                aid = cat.id
                name = cat.name
                phone = cat.phone
                city = cat.city
                pet_name = cat.pet_name
                pet_id = cat.pet_id
            if ce is not None:
                print("2")
                cat = CatEmergency.query.filter(CatEmergency.id == ce).first()
                cat.status = user_in_db.id
                db.session.commit()
                pt = 1
                at = 1
                aid = cat.id
                name = cat.name
                phone = cat.phone
                city = cat.city
                pet_name = cat.pet_name
                pet_id = cat.pet_id
                priority = 1
            if d is not None:
                print("3")
                dog = DogAppointment.query.filter(DogAppointment.id == d).first()
                dog.status = user_in_db.id
                db.session.commit()
                pt = 2
                at = 2
                aid = dog.id
                name = dog.name
                phone = dog.phone
                city = dog.city
                pet_name = dog.pet_name
                pet_id = dog.pet_id
            if de is not None:
                dog = DogEmergency.query.filter(DogEmergency.id == de).first()
                dog.status = user_in_db.id
                db.session.commit()
                print(dog.status)
                pt = 1
                at = 1
                aid = dog.id
                name = dog.name
                phone = dog.phone
                city = dog.city
                pet_name = dog.pet_name
                pet_id = dog.pet_id
                priority = 1

            new_handle = HandleDetails(appointment_id=aid, pet_type=pt, appointment_type=at,
                                       employee_name=form.name.data,
                                       date=form.date.data, employee_id=user_in_db.id, name=name, phone=phone,
                                       city=city,
                                       pet_name=pet_name, pet_id=pet_id, priority=priority)
            db.session.add(new_handle)
            db.session.commit()
            flash(gettext("Appointment handled successfully"))
            return redirect(url_for('orders'))
        return render_template('handle_details.html', title=gettext('handle detials'), form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


@app.route('/handled_appointment', methods=['GET', 'POST'])
def handled_appointment():
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'handled_appointment'
        user_in_db = Employee.query.filter(Employee.employee_number == session.get("NUMBER")).first()
        order_details = HandleDetails.query.filter(HandleDetails.employee_id == user_in_db.id).all()
        print(order_details[0].date)
        b = sorted(order_details, key=lambda x: (-x.priority, x.date), )
        return render_template('handled_appointment.html', title=gettext('handled_appointment'),
                               order_details=b)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


@app.route('/delete_order', methods=['GET', 'POST'])
def delete_order():
    session['currentPage'] = 'delete_order'
    id = request.args.get("id")
    appointment = HandleDetails.query.filter(HandleDetails.id == id).first()
    if appointment.appointment_type == 1 and appointment.pet_type == 1:
        ce = CatEmergency.query.filter(CatEmergency.id == appointment.appointment_id).first()
        ce.status = 0
        db.session.delete(appointment)
        db.session.commit()
    if appointment.appointment_type == 1 and appointment.pet_type == 2:
        de = DogEmergency.query.filter(DogEmergency.id == appointment.appointment_id).first()
        de.status = 0
        db.session.delete(appointment)
        db.session.commit()
    if appointment.appointment_type == 2 and appointment.pet_type == 1:
        cn = CatAppointment.query.filter(CatAppointment.id == appointment.appointment_id).first()
        cn.status = 0
        db.session.delete(appointment)
        db.session.commit()
    if appointment.appointment_type == 2 and appointment.pet_type == 2:
        print(appointment.id)
        dn = DogAppointment.query.filter(DogAppointment.id == appointment.appointment_id).first()
        dn.status = 0
        db.session.delete(appointment)
        db.session.commit()
    return redirect(url_for('orders'))


@app.route('/prioritize', methods=['GET', 'POST'])
def prioritize():
    id = request.args.get("id2")
    appointment = HandleDetails.query.filter(HandleDetails.id == id).first()
    print(appointment.id)
    if appointment.priority == 1 or appointment.priority == 0:
        appointment.priority = 3
        db.session.commit()
    else:
        flash("This appointment is already prioritized")
    return redirect(url_for('handled_appointment'))


@app.route('/cancel_prioritize', methods=['GET', 'POST'])
def cancel_prioritize():
    id = request.args.get("id3")
    appointment = HandleDetails.query.filter(HandleDetails.id == id).first()
    print(appointment.id)
    if appointment.priority == 3:
        if appointment.appointment_type == 2:
            appointment.priority = 0
        if appointment.appointment_type == 1:
            appointment.priority = 1
        db.session.commit()
    else:
        flash('This appointment has not been prioritized')
    return redirect(url_for('handled_appointment'))


@app.route('/qa_e', methods=['GET', 'POST'])
def qa_e():
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'qa_e'
        prev_questions = Question.query.filter().all()
        return render_template('qa_e.html', title=gettext('Q&A'), prev_questions=prev_questions)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'answer'
        form = PostAnswerForm()
        q = request.args.get("q")
        # print(q)
        prev_questions = Question.query.filter(Question.id == q).all()
        prev_answers = Answer.query.filter(Answer.question_id == q).all()
        if form.validate_on_submit():
            postbody = form.postbody.data
            employee_in_db = Employee.query.filter(Employee.employee_number == session.get("NUMBER")).first()
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
        return render_template('answer.html', title=gettext('Q&A'), prev_questions=prev_questions, form=form,
                               prev_answers=prev_answers)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


def takeDate(elem):
    return elem.date


@app.route('/employee_track', methods=['GET', 'POST'])
def employee_track():
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'employee_track'
        user_in_db = Employee.query.filter(Employee.employee_number == session.get("NUMBER")).first()
        t_pets = HandleDetails.query.filter(HandleDetails.employee_id == user_in_db.id).all()
        # print(t_pets[0].date < t_pets[1].date)
        t_pets.sort(key=takeDate)
        return render_template('employee_track.html', title=gettext('track'), t_pets=t_pets)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


@app.route('/customer_track')
def customer_track():
    session['currentPage'] = 'customer_track'
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        owner_id = user_in_db.id
        handled = set()
        nhandled = set()
        cas = CatAppointment.query.filter(CatAppointment.customer_id == owner_id).all()
        for ca in cas:
            if ca.status == 1:
                ha = HandleDetails.query.filter(
                    and_(HandleDetails.pet_type == 1,
                         and_(HandleDetails.appointment_type == 2, HandleDetails.appointment_id == ca.id))).first()
                handled.add(ha)
            else:
                nhandled.add(ca)

        das = DogAppointment.query.filter(DogAppointment.customer_id == owner_id).all()
        for da in das:
            if da.status == 1:
                ha = HandleDetails.query.filter(
                    and_(HandleDetails.pet_type == 2,
                         and_(HandleDetails.appointment_type == 2, HandleDetails.appointment_id == da.id))).first()
                handled.add(ha)
            else:
                nhandled.add(da)

        ces = CatEmergency.query.filter(CatEmergency.customer_id == owner_id).all()
        for ce in ces:
            if ce.status == 1:
                ha = HandleDetails.query.filter(
                    and_(HandleDetails.pet_type == 1,
                         and_(HandleDetails.appointment_type == 1, HandleDetails.appointment_id == ce.id))).first()
                handled.add(ha)
            else:
                nhandled.add(ce)

        des = DogEmergency.query.filter(DogEmergency.customer_id == owner_id).all()
        for de in des:
            if de.status == 1:
                ha = HandleDetails.query.filter(
                    and_(HandleDetails.pet_type == 2,
                         and_(HandleDetails.appointment_type == 1, HandleDetails.appointment_id == de.id))).first()
                handled.add(ha)
            else:
                nhandled.add(de)

        return render_template('customer_track.html', title=gettext('track'), nha=nhandled, ha=handled)
    else:
        flash(gettext("User needs to either login or signup first"))
        return redirect(url_for('login'))


@app.route('/start_treatment', methods=['GET', 'POST'])
def start_treatment():
    pid = request.args.get("p")
    print(pid)
    t_pets = HandleDetails.query.filter(HandleDetails.id == pid).first()
    if t_pets.treatment_date == 'Undetermined':
        dt = datetime.datetime.now()
        time = str(dt)
        time = time[:16]
        t_pets.treatment_date = time
        t_pets.finish_date = 'In treatment'
        db.session.commit()
    return redirect(url_for('employee_track'))


@app.route('/finish_treatment', methods=['GET', 'POST'])
def finish_treatment():
    pid = request.args.get("p2")
    print(pid)
    t_pets = HandleDetails.query.filter(HandleDetails.id == pid).first()
    if t_pets.finish_date == 'In treatment':
        dt = datetime.datetime.now()
        time = str(dt)
        time = time[:16]
        t_pets.finish_date = time
        db.session.commit()
    if t_pets.finish_date == 'Undetermined':
        flash("This treatment haven't start yet")
    return redirect(url_for('employee_track'))


@app.route('/leave_hospital', methods=['GET', 'POST'])
def leave_hospital():
    pid = request.args.get("p4")
    t_pets = HandleDetails.query.filter(HandleDetails.id == pid).first()
    if t_pets.leave_date != 'Undetermined':
        flash("This pet has already leave the hospital")
    if t_pets.finish_date != 'Undetermined' and t_pets.finish_date != 'In treatment':
        dt = datetime.datetime.now()
        time = str(dt)
        time = time[:16]
        t_pets.leave_date = time
        db.session.commit()
    else:
        flash("This pet haven't finish treatment yet")
    return redirect(url_for('employee_track'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    pid = request.args.get("p3")
    print(pid)
    t_pets = HandleDetails.query.filter(HandleDetails.id == pid).first()
    if t_pets.finish_date != 'Undetermined' and t_pets.finish_date != 'In treatment':
        flash(gettext("This treatment has already finished, you cannot reset it"))
    else:
        t_pets.treatment_date = 'Undetermined'
        t_pets.finish_date = 'Undetermined'
        db.session.commit()
    return redirect(url_for('employee_track'))


@app.route('/pet_details', methods=['GET', 'POST'])
def pet_details():
    # print(1)
    if not session.get("NUMBER") is None:
        session['currentPage'] = 'pet_details'
        pid = request.args.get("pid")
        t_pets = HandleDetails.query.filter(HandleDetails.id == pid).all()
        return render_template('pet_details.html', title=gettext('pet_details'), t_pets=t_pets)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('index'))


@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    session['currentPage'] = 'add_pet'
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
                flash(gettext("Post successfully"))
                return redirect(url_for('my_pets'))
            else:
                flash(gettext("The image format is wrong, please upload it again."))
                return redirect(url_for('add_pet'))
        else:
            flash(gettext("User needs to either login or signup first"))
            return redirect(url_for('login'))
    return render_template('add_pet.html', title=gettext('Add Pet'), form=form)


@app.route('/my_pets')
def my_pets():
    session['currentPage'] = 'my_pets'
    if not session.get("USERNAME") is None:
        user_in_db = Customer.query.filter(Customer.username == session.get("USERNAME")).first()
        pet = Pet.query.filter(Pet.owner_id == user_in_db.id)
        return render_template('my_pets.html', title=gettext('My Pets'), pet=pet)
    else:
        flash(gettext("User needs to either login or signup first"))
        return redirect(url_for('login'))
    return render_template('my_pets.html', title=gettext('My Pets'), pet=pet)


@app.route('/pet_detail', methods=['GET', 'POST'])
def pet_detail():
    session['currentPage'] = 'pet_detail'
    pet = request.args.get("pet")
    session['petID'] = pet
    pet = Pet.query.filter(Pet.id == pet)
    return render_template('pet_detail.html', title=gettext('Detail'), pet=pet)


@app.route('/pet_delete', methods=['GET', 'POST'])
def pet_delete():
    session['currentPage'] = 'my_pets'
    pet = request.args.get("pet")
    session['petID'] = pet
    pet_delete = Pet.query.filter(Pet.id == pet).first()
    db.session.delete(pet_delete)
    db.session.commit()
    return redirect(url_for('my_pets'))
