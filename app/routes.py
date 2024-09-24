from flask import render_template, redirect, url_for, flash,Blueprint,abort, session
# from forms import RegistrationForm,SignInForm
bp = Blueprint('main', __name__)

user_data = {}

@bp.route('/')
def index():
    return render_template('home.html')


