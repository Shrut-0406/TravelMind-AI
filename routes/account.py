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
        .all()
    )


    return render_template(
        "account.html",
        trips=user_trips
    )