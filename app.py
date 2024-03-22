from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # In real app, hash passwords

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')  # Hash in real app
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('register.html')

@app.route('/success')
def success():
    return 'Registration successful!'

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
