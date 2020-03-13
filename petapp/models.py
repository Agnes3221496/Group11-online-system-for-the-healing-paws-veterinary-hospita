from datetime import datetime
from petapp import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

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