from . import db  # Import the db instance from your Flask app

class User(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(40), nullable=False)  # Consider hashing

class Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime, nullable=False)
    language = db.Column(db.String(25), nullable=False)
    service = db.Column(db.String(40), nullable=False)
    street_address = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(40), nullable=False)
    state_district_abbrv = db.Column(db.String(4), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
