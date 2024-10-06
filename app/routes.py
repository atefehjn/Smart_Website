from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    Blueprint,
    abort,
    session,
    request,
)
from flask_sqlalchemy import SQLAlchemy
from .create_db import db, User, bcrypt,Prediction
from .ml_prediction import prediction
from .input_form import InputForm
from datetime import datetime,timezone

# from forms import RegistrationForm,SignInForm
bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("home.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("You already have an account. Please log in.", "warning")
            return redirect(url_for("main.register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful, please Login. Thank you", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("This username is not registered. Please Register.", "warning")
            return redirect(url_for("main.login"))
        
        if user and bcrypt.check_password_hash(user.password, password):
            session["username"] = user.username
            flash("Login successful!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Login failed. Please check your username and password.", "danger")
            return redirect(url_for("main.login"))

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.pop("username",None)
    session.clear()
    flash("You are logged out", "success")

    return redirect(url_for("main.index"))


def login_required(f):
    def wrap(*args, **kwargs):
        if "username" not in session:
            flash("You need to login first!", "danger")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


@bp.route("/input", methods=["GET", "POST"])
@login_required
def input_data():
    form = InputForm()
    if request.method == "POST":
        if form.validate_on_submit():
            features = [
                float(request.form["mean_radius"]),
                float(request.form["mean_texture"]),
                float(request.form["mean_perimeter"]),
                float(request.form["mean_area"]),
            ]
            feature_values = [features]

            # Get the prediction from your machine learning model
            result = prediction(feature_values)
            if result[0] == 0:
                predicted_cancer = "Malignant"
                explanation = "Malignant tumors are cancerous, aggressive and can grow uncontrollably."
            else:
                predicted_cancer = "Benign"
                explanation = "Benign tumors are noncancerous. They stay in their primary location without invading other sites of the body."

            # Get the current user's ID
            current_user = User.query.filter_by(username=session["username"]).first()
            user_id = current_user.id

            # Create a new Prediction entry
            new_prediction = Prediction(
                user_id=user_id,
                mean_radius=features[0],  # Save the individual feature values
                mean_texture=features[1],
                mean_perimeter=features[2],
                mean_area=features[3],
                prediction_result=predicted_cancer,
                timestamp=datetime.now(timezone.utc)  # Ensure timestamp is set correctly
            )

            # Add the new prediction to the database
            db.session.add(new_prediction)
            db.session.commit()

            return render_template(
                "result.html",
                Cancer_prediction=predicted_cancer,
                Explanation=explanation,
            )

    return render_template("input.html", form=form)

@bp.route("/history", methods=["GET"])
@login_required
def prediction_history():
    
    current_user = User.query.filter_by(username=session["username"]).first()
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    return render_template("history.html", predictions=predictions)

# @bp.route('/result')
# @login_required
# def result():
#     #dispaly outputed result.
#     return render_template('result.html')
