# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, User  # Ensure you have these models defined as per previous instructions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-azure-database-connection-string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Capture form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']  # Remember to hash passwords in a real application

        # Create a new User instance
        new_user = User(name=name, email=email, phone=phone, password=password)
        
        # Add to the database session and commit
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('success'))  # Redirect or handle as needed
    return render_template('register.html')

@app.route('/success')
def success():
    return 'Registration successful!'

if __name__ == '__main__':
    app.run(debug=True)
