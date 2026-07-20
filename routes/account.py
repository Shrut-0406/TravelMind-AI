from flask import Blueprint, render_template
from flask_login import login_required, current_user

from database.models import Trip


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