from database.database import db


class Trip(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    start = db.Column(
        db.String(100),
        nullable=False
    )


    destination = db.Column(
        db.String(100),
        nullable=False
    )


    days = db.Column(
        db.Integer,
        nullable=False
    )


    budget = db.Column(
        db.Float,
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )