from datetime import datetime
from smtplib import SMTP
from smtplib import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from requests import Session
from flask import current_app
from speedtest_servers.models import Servers
from speedtest_servers.models import Settings
from speedtest_servers.models import Users

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"
}


def get_servers():
    with Session() as s:
        page_src = s.get(
            "https://c.speedtest.net/speedtest-servers-static.php",
            headers=headers
        )

    soup = BeautifulSoup(page_src.content, "lxml")
    servers = soup.select("servers server")

    return servers


def create_or_update():
    Servers.delete().execute(None)
    settings = Settings.get()
    settings.updated_at = datetime.today()
    settings.is_updating = True
    settings.save()

    list_servers = get_servers()
    for i in list_servers:
        Servers.create(
            server_id=i.get("id"),
            city=i.get("name"),
            country=i.get("country"),
            provider=i.get("sponsor")
        )

    settings.is_updating = False
    settings.save()


def send_admin_credentials():
    config = current_app.config
    users = Users.get()
    username = users.username
    access_key = users.access_key

    smtp_server = config["SMTP_SERVER"]
    port = config["SMTP_PORT"]
    sender_email = config["SENDER_EMAIL"]
    receiver_email = config["RECEIVER_EMAIL"]
    password = config["EMAIL_PASSWORD"]

    subject = "[Speedtest Servers] Admin credentials"
    body = f"""
    Your credentials:

    Username: {username}
    Access Key: {access_key}
    """

    message = MIMEMultipart()
    message["From"] = "Speedtest Servers"
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()

    context = ssl.create_default_context()
    with SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
