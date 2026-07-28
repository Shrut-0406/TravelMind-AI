from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


from flask_login import UserMixin


class User(db.Model, UserMixin):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )


    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )


    password = db.Column(
        db.String(255),
        nullable=False
    )


    def set_password(self, password):

        self.password = generate_password_hash(password)


    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )


class Trip(db.Model):

    __tablename__ = "trips"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey("users.id"),
    nullable=False
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

    traveler_type = db.Column(
        db.String(50),
        nullable=True
    )

    image_url = db.Column(
        db.String(500),
        nullable=True
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

    map_locations = db.Column(
        db.JSON
    )

    route_coordinates = db.Column(
        db.JSON
    )

    hotel_options = db.Column(
        db.JSON
    )
    selected_hotel = db.Column(
        db.JSON
    )