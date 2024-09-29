from flask import Flask, render_template, redirect, url_for, flash,Blueprint,abort, session, request
from flask_sqlalchemy import SQLAlchemy
from .create_db import db, User, bcrypt
from .ml_prediction import prediction
from .input import PredictionForm

# from forms import RegistrationForm,SignInForm
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')   

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)  
        db.session.commit()
        flash("Registration successful, please Login. Thank you", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('main.predict'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            return redirect(url_for('main.login'))  

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('username')
    flash("You are logged out", "success")

    return(redirect(url_for('main.login')))


def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            flash('You need to login first!', 'danger')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@bp.route('/predict' ,methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictionForm()
    if form.validate_on_submit():
        mean_radius = form.mean_radius.data
        mean_texture = form.mean_texture.data
        mean_perimeter = form.mean_perimeter.data
        mean_area = form.mean_area.data

        # Assuming you have some function that handles predictions
        data = [[mean_radius, mean_texture, mean_perimeter, mean_area]]
        result = prediction(data)

        if result[0] == 0:
            result = "Malignant"
        else:
            result = "Benign"

        flash(f'Prediction Result: {result}', 'success')
        return redirect(url_for('main.predict'))

    return render_template('input.html', form=form)