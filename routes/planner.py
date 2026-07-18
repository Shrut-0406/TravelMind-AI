from flask import Blueprint, render_template, request

from services.ai_service import generate_trip_plan

from database.database import db
from database.models import Trip

from datetime import datetime
import json


planner = Blueprint("planner", __name__)


@planner.route("/planner")
def planner_page():

    return render_template("planner.html")



@planner.route("/generate", methods=["POST"])
def generate():

    # Trip Information
    origin = request.form["origin"]

    destination = request.form["destination"]


    # Dates
    start_date = datetime.strptime(
        request.form["start_date"],
        "%Y-%m-%d"
    )

    end_date = datetime.strptime(
        request.form["end_date"],
        "%Y-%m-%d"
    )


    if end_date < start_date:
        return "End date cannot be before start date."


    days = (end_date - start_date).days + 1


    # Travelers
    adults = int(
        request.form["adults"]
    )

    children = int(
        request.form["children"]
    )


    # Budget
    budget = float(
        request.form["budget"]
    )


    # Preferences
    transportation = request.form["transportation"]

    accommodation = request.form["accommodation"]


    interests = request.form.getlist(
        "interests"
    )


    trip_goal = request.form["trip_goal"]


    # Convert interests list to JSON text
    interests_json = json.dumps(interests)



    # Save trip to database
    new_trip = Trip(

        origin=origin,

        destination=destination,

        start_date=start_date,

        end_date=end_date,

        days=days,

        adults=adults,

        children=children,

        budget=budget,

        transportation=transportation,

        accommodation=accommodation,

        interests=interests_json,

        trip_goal=trip_goal
    )


    db.session.add(new_trip)

    db.session.commit()



    # Temporary AI response
    trip_plan = generate_trip_plan(
        destination,
        start_date,
        end_date,
        days,
        budget
    )



    return render_template(
        "trip_result.html",

        origin=origin,

        destination=destination,

        start_date=start_date.strftime("%Y-%m-%d"),

        end_date=end_date.strftime("%Y-%m-%d"),

        days=days,

        adults=adults,

        children=children,

        budget=budget,

        transportation=transportation,

        accommodation=accommodation,

        interests=interests,

        trip_goal=trip_goal,

        trip_plan=trip_plan
    )