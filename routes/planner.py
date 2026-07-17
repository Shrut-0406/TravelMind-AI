from flask import Blueprint, render_template, request

from services.ai_service import generate_trip_plan

from database.database import db
from database.models import Trip


planner = Blueprint("planner", __name__)


@planner.route("/planner")
def planner_page():

    return render_template("planner.html")


@planner.route("/generate", methods=["POST"])
def generate():

    start = request.form["start"]

    destination = request.form["destination"]

    days = request.form["days"]

    budget = request.form["budget"]


    new_trip = Trip(
        start=start,
        destination=destination,
        days=days,
        budget=budget
    )


    db.session.add(new_trip)

    db.session.commit()


    trip_plan = generate_trip_plan(
        destination,
        days,
        budget
    )


    return render_template(
        "trip_result.html",
        start=start,
        destination=destination,
        days=days,
        budget=budget,
        trip_plan=trip_plan
    )