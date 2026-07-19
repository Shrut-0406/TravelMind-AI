from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user

from database.database import db
from database.models import User

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":

        return render_template("register.html")


    username = request.form["username"].strip()

    email = request.form["email"].strip().lower()

    password = request.form["password"]

    confirm_password = request.form["confirm_password"]


    if password != confirm_password:

        return "Passwords do not match."


    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:

        return "Username already exists."


    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:

        return "Email already registered."


    user = User(

        username=username,

        email=email

    )

    user.set_password(password)


    db.session.add(user)

    db.session.commit()


    return redirect(
        url_for("auth.login")
    )

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template("login.html")


    email = request.form["email"].strip().lower()

    password = request.form["password"]


    user = User.query.filter_by(
        email=email
    ).first()


    if not user:

        return "Invalid email or password."


    if not user.check_password(password):

        return "Invalid email or password."


    login_user(user)

    return redirect("/")

    session["username"] = user.username


    return redirect(
        url_for("planner.planner_page")
    )