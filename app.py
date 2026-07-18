from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from database.database import db


def create_app():

    app = Flask(__name__)


    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travelmind.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)


    from routes.main import main
    from routes.planner import planner


    app.register_blueprint(main)
    app.register_blueprint(planner)


    with app.app_context():

        db.create_all()


    return app



if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)