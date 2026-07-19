from flask import Blueprint, render_template, redirect, url_for

from database.database import db
from database.models import Trip


history = Blueprint("history", __name__)


@history.route("/trips")
def trips():

    all_trips = (
        Trip.query
        .order_by(Trip.created_at.desc())
        .all()
    )

    return render_template(
        "trip_history.html",
        trips=all_trips
    )


@history.route("/trip/<int:trip_id>")
def view_trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    return render_template(
        "saved_trip.html",
        trip=trip
    )


@history.route("/delete-trip/<int:trip_id>")
def delete_trip(trip_id):

    trip = Trip.query.get_or_404(trip_id)

    db.session.delete(trip)
    db.session.commit()

    return redirect(url_for("history.trips"))