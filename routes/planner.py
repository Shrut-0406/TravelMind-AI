from flask import Blueprint, render_template, request

from flask_login import login_required, current_user


from services.ai_service import generate_trip_plan
from services.image_service import get_destination_image
from services.budget_service import analyze_budget
from services.map_service import get_coordinates


from database.database import db
from database.models import Trip


from datetime import datetime

import json



planner = Blueprint(
    "planner",
    __name__
)




@planner.route("/planner")
def planner_page():

    return render_template(
        "planner.html"
    )





@planner.route("/generate", methods=["POST"])
@login_required
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



    days = (
        end_date - start_date
    ).days + 1





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

    transportation = request.form[
        "transportation"
    ]


    accommodation = request.form[
        "accommodation"
    ]



    interests = request.form.getlist(
        "interests"
    )



    trip_goal = request.form[
        "trip_goal"
    ]

    traveler_type = request.form[
        "traveler_type"
        ]




    interests_json = json.dumps(
        interests
    )





    # Destination image

    image_url = get_destination_image(
        destination
    )

    origin_lat, origin_lon = get_coordinates(
        origin
    )

    destination_lat, destination_lon = get_coordinates(
        destination
    )



    # Budget Analysis
    budget_analysis = analyze_budget(

        budget=budget,

        adults=adults,

        children=children,

        days=days,

        transportation=transportation,

        accommodation=accommodation

    )



    # AI Generation

    trip_plan = generate_trip_plan(


        origin=origin,


        destination=destination,


        start_date=start_date.strftime(
            "%Y-%m-%d"
        ),


        end_date=end_date.strftime(
            "%Y-%m-%d"
        ),


        days=days,


        adults=adults,


        children=children,


        budget=budget,


        transportation=transportation,


        accommodation=accommodation,


        interests=interests,


        trip_goal=trip_goal,

        budget_analysis=budget_analysis,

        traveler_type=traveler_type,

    )







    # Save trip

    new_trip = Trip(


        user_id=current_user.id,


        origin=origin,


        destination=destination,


        image_url=image_url,


        start_date=start_date,


        end_date=end_date,


        days=days,


        adults=adults,


        children=children,


        budget=budget,


        transportation=transportation,


        accommodation=accommodation,


        interests=interests_json,


        trip_goal=trip_goal,


        trip_plan=trip_plan

    )





    db.session.add(
        new_trip
    )


    db.session.commit()






    return render_template(

        "trip_result.html",


        origin=origin,


        destination=destination,


        image_url=image_url,


        start_date=start_date.strftime(
            "%Y-%m-%d"
        ),


        end_date=end_date.strftime(
            "%Y-%m-%d"
        ),


        days=days,


        adults=adults,


        children=children,


        budget=budget,


        transportation=transportation,


        accommodation=accommodation,


        interests=interests,


        trip_goal=trip_goal,


        trip_plan=trip_plan,


        origin_lat=origin_lat,

        origin_lon=origin_lon,


        destination_lat=destination_lat,

        destination_lon=destination_lon,

    )