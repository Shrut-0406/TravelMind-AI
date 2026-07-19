from flask import Blueprint, render_template, redirect, url_for

from flask_login import login_required, current_user

from database.database import db
from database.models import Trip


history = Blueprint("history", __name__)


@history.route("/trips")
@login_required
def trips():

    user_trips = (
        Trip.query
        .filter_by(user_id=current_user.id)
        .order_by(Trip.created_at.desc())
        .all()
    )

    return render_template(
        "trip_history.html",
        trips=user_trips
    )



@history.route("/trip/<int:trip_id>")
@login_required
def view_trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)


    # Security check:
    # Prevent user A from viewing user B's trip
    if trip.user_id != current_user.id:
        return "Unauthorized", 403


    return render_template(
        "saved_trip.html",
        trip=trip
    )



@history.route("/delete-trip/<int:trip_id>")
@login_required
def delete_trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)


    # Security check:
    # Prevent deleting someone else's trip
    if trip.user_id != current_user.id:
        return "Unauthorized", 403


    db.session.delete(trip)
    db.session.commit()


    return redirect(
        url_for("history.trips")
    )