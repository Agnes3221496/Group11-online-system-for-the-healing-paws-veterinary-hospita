from datetime import datetime
from petapp import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cat_appointment = db.relationship('CatAppointment', backref='customer', lazy='dynamic')
    dog_appointment = db.relationship('DogAppointment', backref='customer', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_number = db.Column(db.Integer(), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class CatAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    phone = db.Column(db.Integer())
    city = db.Column(db.String(10))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    status = db.Column(db.Integer(),default=0)
    pet_name = db.Column(db.String(32))
    # pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __repr__(self):
        return '<name {}>, <phone {}>, <city {}>'.format(self.name, self.phone, self.city)


class DogAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    phone = db.Column(db.Integer())
    city = db.Column(db.String(10))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    status = db.Column(db.Integer(),default=0)
    pet_name = db.Column(db.String(32))
    # pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __repr__(self):
        return '<name {}>, <phone {}>, <city {}>'.format(self.name, self.phone, self.city)


class CatEmergency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    phone = db.Column(db.Integer())
    city = db.Column(db.String(10))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    status = db.Column(db.Integer(),default=0)
    pet_name = db.Column(db.String(32))
    # pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __repr__(self):
        return '<name {}>, <phone {}>, <city {}>'.format(self.name, self.phone, self.city)


class DogEmergency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    phone = db.Column(db.Integer())
    city = db.Column(db.String(10))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    status = db.Column(db.Integer(), default=0)
    pet_name = db.Column(db.String(32))
    # pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))

    def __repr__(self):
        return '<name {}>, <phone {}>, <city {}>'.format(self.name, self.phone, self.city)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisher = db.Column(db.Integer, db.ForeignKey(Customer.id))
    title = db.Column(db.String(120), index=True)
    detail = db.Column(db.String(300), index=True)
    image = db.Column(db.String(256))
    publish_date = db.Column(db.DATETIME)

    def __repr__(self):
        return '<Question {}>'.format(self.title)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(140))
    time = db.Column(db.String(140))
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.employee_number'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer,index=True)
    species = db.Column(db.String(64), index=True)
    image = db.Column(db.String(256))
    # cat_standard = db.relationship('CatAppointment', backref='pet', lazy='dynamic')
    # dog_standard = db.relationship('DogAppointment', backref='pet', lazy='dynamic')
    # cat_emergency = db.relationship('CatEmergency', backref='pet', lazy='dynamic')
    # cat_emergency = db.relationship('DogEmergency', backref='pet', lazy='dynamic')


    def __repr__(self):
        return '{}'.format(self.name)