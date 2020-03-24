from flask import Flask
from shorter_app.apis import api
from shorter_app.config import DefaultConfig
from shorter_app.database import init_db
from shorter_app.authorization import init_user


def create_app(config=DefaultConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    api._doc = app.config.get("SWAGGER_DOC_PATH")
    api.init_app(
        app,
        title="Shorter Application",
        version="0.0.1",
        description="Microservice for translate URL in a shorter URL",
    )

    init_db(app)

    @app.teardown_request
    def teardown_request(request):
        app.db_session.remove()

    app.before_request(init_user)
    return app
