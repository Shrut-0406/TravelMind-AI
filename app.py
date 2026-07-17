from flask import Flask


def create_app():

    app = Flask(__name__)


    from routes.main import main
    from routes.planner import planner


    app.register_blueprint(main)

    app.register_blueprint(planner)


    return app



if __name__ == "__main__":

    app = create_app()

    app.run(debug=True)