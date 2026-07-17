from flask import Blueprint, render_template, request


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


    return render_template(
        "trip_result.html",
        start=start,
        destination=destination,
        days=days,
        budget=budget
    )