from speedtest_servers.models import database
from speedtest_servers.models import Servers
from speedtest_servers.models import Users
from speedtest_servers.models import Settings
from speedtest_servers.views.main import create_or_update


def initialize_database(app):
    database.init(
        app.config["DB_NAME"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        host=app.config["DB_HOST"],
    )


@database.connection_context()
def prepare_database():
    database.create_tables([Servers, Settings, Users])

    if not Users.get_or_none(username="Admin"):
        Users.create(username="Admin")

    if not Settings.select():
        Settings.create()
