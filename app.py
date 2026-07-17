from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/planner")
def planner():
    return render_template("planner.html")


@app.route("/generate", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True)