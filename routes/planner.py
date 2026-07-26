from flask import Blueprint, render_template, request

from flask_login import login_required, current_user

from services.ai_service import generate_trip_plan
from services.budget_service import analyze_budget
from services.map_service import get_coordinates
from services.weather_service import get_weather_forecast
from services.trip_builder import rebuild_trip_data

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


    # -------------------------
    # Trip Information
    # -------------------------

    origin = request.form["origin"]

    destination = request.form["destination"]



    # -------------------------
    # Dates
    # -------------------------

    start_date = datetime.strptime(
        request.form["start_date"],
        "%Y-%m-%d"
    )


    end_date = datetime.strptime(
        request.form["end_date"],
        "%Y-%m-%d"
    )


    if end_date < start_date:

        return "End date cannot be before start date"



    days = (
        end_date - start_date
    ).days + 1



    # -------------------------
    # Travelers
    # -------------------------

    adults = int(
        request.form["adults"]
    )


    children = int(
        request.form["children"]
    )



    # -------------------------
    # Budget
    # -------------------------

    budget = float(
        request.form["budget"]
    )



    # -------------------------
    # Preferences
    # -------------------------

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



    # -------------------------
    # Coordinates + Weather
    # -------------------------

    origin_lat, origin_lon = get_coordinates(
        origin
    )


    destination_lat, destination_lon = get_coordinates(
        destination
    )


    weather_forecast = []


    if destination_lat and destination_lon:

        weather_forecast = get_weather_forecast(

            destination_lat,

            destination_lon

        )



    # -------------------------
    # Budget Analysis
    # -------------------------

    budget_analysis = analyze_budget(

        budget=budget,

        adults=adults,

        children=children,

        days=days,

        transportation=transportation,

        accommodation=accommodation

    )



    # -------------------------
    # AI Generation
    # -------------------------

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

        weather_forecast=weather_forecast

    )



    # -------------------------
    # Create database object
    # -------------------------

    new_trip = Trip(

        user_id=current_user.id,

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

        trip_goal=trip_goal,

        traveler_type=traveler_type,

        trip_plan=trip_plan

    )



    # -------------------------
    # Build derived data
    # -------------------------

    weather_forecast = rebuild_trip_data(
        new_trip
    )



    db.session.add(
        new_trip
    )


    db.session.commit()



    print("MAP:")
    print(new_trip.map_locations)

    print("ROUTE:")
    print(new_trip.route_coordinates)



    return render_template(

        "trip_result.html",

        origin=origin,

        destination=destination,

        image_url=new_trip.image_url,

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

        traveler_type=traveler_type,

        trip_plan=trip_plan,

        origin_lat=origin_lat,

        origin_lon=origin_lon,

        destination_lat=destination_lat,

        destination_lon=destination_lon,

        map_locations=new_trip.map_locations,

        route_coordinates=new_trip.route_coordinates,

        weather_forecast=weather_forecast,

        trip_id=new_trip.id

    )