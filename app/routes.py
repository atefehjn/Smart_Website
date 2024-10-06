from flask import Flask, render_template, redirect, url_for, flash,Blueprint,abort, session, request
from flask_sqlalchemy import SQLAlchemy
from .create_db import db, User, bcrypt


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
        
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('main.register'))  
        
        
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
            return redirect(url_for('main.inputdata'))
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


@bp.route('/input')
@login_required
def inputdata():
    if 'username' not in session:
        flash('You need to log in first!', 'danger')
        return redirect(url_for('main.login'))
    return "Input Data Page Content"


@bp.route('/predict')
@login_required
def predict():
    if 'username' not in session:
        flash('You need to log in first!', 'danger')
        return redirect(url_for('main.login'))
   
    


    return "Here is predict page"











