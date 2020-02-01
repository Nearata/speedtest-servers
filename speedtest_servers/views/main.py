from datetime import datetime
from datetime import timedelta
from flask import Blueprint
from flask import render_template
from flask import request
from speedtest_servers.models import Servers
from speedtest_servers.models import Settings
from speedtest_servers.models import Users
from speedtest_servers.utils import create_or_update
from speedtest_servers.utils import send_admin_credentials

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    settings = Settings.get()
    last_update = settings.updated_at
    next_update = settings.updated_at + timedelta(days=1)
    updating = settings.is_updating

    return render_template(
        "home.html",
        page_title="Server list",
        updated_at=last_update,
        next_update_available=next_update,
        is_updating=updating
    )


@bp.route("/servers")
def servers():
    lst = {"data": []}
    srv = Servers.select()
    settings = Settings.get()

    if not settings.is_initialized:
        settings.is_initialized = True
        settings.save()
        send_admin_credentials()
        create_or_update()

    if srv and not settings.is_updating:
        for i in srv:
            lst["data"].append(
                {
                    "id": i.server_id,
                    "city": i.city,
                    "country": i.country,
                    "provider": i.provider
                }
            )

    return lst


@bp.route("/servers/update", methods=["POST"])
def user_servers_update():
    settings = Settings.get()
    
    if datetime.today() > settings.updated_at + timedelta(days=1):
        create_or_update()
        return "Update done."

    return "The servers table has been shortly updated.", 429


@bp.route("/admin")
def admin():
    return render_template(
        "admin.html",
        page_title="ADMIN"
    )


@bp.route("/admin/servers/update/", methods=["POST"])
def admin_servers_update():
    errors = []

    if not request.form["username"]:
        errors.append("Username is required.")

    if not request.form["access_key"]:
        errors.append("Access Key is required")

    username = request.form["username"]
    access_key = request.form["access_key"]

    user_data = Users.get_or_none(username=username)

    if not user_data:
        errors.append("Username not valid.")
    elif user_data.access_key != access_key:
        errors.append("Access Key not valid.")

    if errors:
        return {
            "errors": errors
        }, 401

    create_or_update()
    
    return "Done."
