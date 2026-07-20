from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user


from database.database import db
from database.models import Trip, User

account = Blueprint(
    "account",
    __name__
)


@account.route("/account")
@login_required
def account_page():

    # Get only current user's trips
    trips = (
        Trip.query
        .filter_by(user_id=current_user.id)
        .order_by(Trip.created_at.desc())
        .all()
    )


    # Statistics
    total_trips = len(trips)

    total_budget = sum(
        trip.budget for trip in trips
    )


    return render_template(
        "account.html",

        trips=trips,

        total_trips=total_trips,

        total_budget=total_budget
    )


@account.route("/account/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()

        # Check username
        existing_username = User.query.filter_by(username=username).first()

        if existing_username and existing_username.id != current_user.id:
            flash("Username already exists.")
            return redirect(url_for("account.edit_profile"))

        # Check email
        existing_email = User.query.filter_by(email=email).first()

        if existing_email and existing_email.id != current_user.id:
            flash("Email already exists.")
            return redirect(url_for("account.edit_profile"))

        current_user.username = username
        current_user.email = email

        db.session.commit()

        flash("Profile updated successfully!")

        return redirect(url_for("account.account_page"))

    return render_template(
        "edit_profile.html",
        user=current_user
    )

@account.route("/account/delete", methods=["POST"])
@login_required
def delete_account():

    user = current_user

    Trip.query.filter_by(
        user_id=user.id
    ).delete()

    db.session.delete(user)

    db.session.commit()

    logout_user()

    flash(
        "Account deleted.",
        "success"
    )

    return redirect(url_for("main.home"))