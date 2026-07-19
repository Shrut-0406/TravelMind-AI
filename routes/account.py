from flask import Blueprint, render_template
from flask_login import login_required, current_user

from database.models import Trip


account = Blueprint("account", __name__)


@account.route("/account")
@login_required
def account_page():

    user_trips = (
        Trip.query
        .filter_by(user_id=current_user.id)
        .order_by(Trip.created_at.desc())
        .limit(5)
        .all()
    )


    trip_count = (
        Trip.query
        .filter_by(user_id=current_user.id)
        .count()
    )


    return render_template(
        "account.html",
        user=current_user,
        trips=user_trips,
        trip_count=trip_count
    )