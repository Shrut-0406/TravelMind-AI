from database.database import db


class Trip(db.Model):

    __tablename__ = "trips"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Trip Locations
    origin = db.Column(
        db.String(100),
        nullable=False
    )

    destination = db.Column(
        db.String(100),
        nullable=False
    )

    # Trip Dates
    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    days = db.Column(
        db.Integer,
        nullable=False
    )

    # Travelers
    adults = db.Column(
        db.Integer,
        nullable=False
    )

    children = db.Column(
        db.Integer,
        nullable=False
    )

    # Budget
    budget = db.Column(
        db.Float,
        nullable=False
    )

    # Preferences
    transportation = db.Column(
        db.String(50),
        nullable=False
    )

    accommodation = db.Column(
        db.String(50),
        nullable=False
    )

    interests = db.Column(
        db.Text,
        nullable=False
    )

    trip_goal = db.Column(
        db.String(50),
        nullable=False
    )

    # AI Generated Trip
    trip_plan = db.Column(
        db.JSON,
        nullable=True
    )

    # Metadata
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )