from flask import Flask
from flask_login import LoginManager, current_user
from dotenv import load_dotenv

import os


load_dotenv()


from database.database import db
from database.models import User


def create_app():

    app = Flask(__name__)


    # Configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///travelmind.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



    # Database
    db.init_app(app)



    # Flask Login
    login_manager = LoginManager()

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"



    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(
            int(user_id)
        )



    # Blueprints
    from routes.main import main
    from routes.planner import planner
    from routes.history import history
    from routes.auth import auth


    app.register_blueprint(main)

    app.register_blueprint(planner)

    app.register_blueprint(history)

    app.register_blueprint(auth)



    # Create database tables
    with app.app_context():

        db.create_all()



    # Header user info
    @app.context_processor
    def inject_user():

        return {

            "logged_in": current_user.is_authenticated,


            "username":
                current_user.username
                if current_user.is_authenticated
                else None

        }



    return app





if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)