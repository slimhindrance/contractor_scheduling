import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Update with your actual PostgreSQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cwl21:Lindy101@llspoc.postgres.database.azure.com/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), unique=False, nullable=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('Username already exists.')
                return redirect(url_for('register'))
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html')
    except SQLAlchemyError as e:
        app.logger.error('Error during registration: %s', str(e))
        flash('A database error occurred. Please try again.')
        return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.email = request.form['email']
        user.phone = request.form['phone']
        db.session.commit()
        flash('Profile updated successfully.')
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
