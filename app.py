from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models after db initialization to avoid circular import issues
from models import User

@app.route('/')
def index():
    return "Hello, welcome to the Flask App!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')  # Remember to hash passwords in a real app

        # Create a new User instance
        new_user = User(name=name, email=email, phone=phone, password=password)
        
        # Add to the database session and commit
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('success'))
    return render_template('register.html')

@app.route('/success')
def success():
    return 'Registration successful!'

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
