from speedtest_servers import create_app
from config import Config

app = create_app(Config)
app.config["ENV"] = "development"


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
