from flask import Flask
from flask_assets import Bundle
from speedtest_servers.views import register_frontend_views
from speedtest_servers.database import initialize_database
from speedtest_servers.database import prepare_database
from speedtest_servers.extensions import assets


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    assets.init_app(app)

    css = Bundle(
        "fonts/roboto/roboto.css",
        "css/bootstrap.min.css",
        "css/dataTables.bootstrap4.min.css",
        "css/select2.min.css",
        "css/style.css",
        filters="cssutils",
        output="css/speedtest-servers.min.css"
    )

    js = Bundle(
        "js/jquery.min.js",
        "js/select2.min.js",
        "js/jquery.dataTables.min.js",
        "js/dataTables.bootstrap4.min.js",
        "js/scripts.js",
        filters="rjsmin",
        output="js/speedtest-servers.min.js"
    )

    assets.register("css", css)
    assets.register("js", js)

    initialize_database(app)
    prepare_database()
    register_frontend_views(app)

    return app
