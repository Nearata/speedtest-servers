from gevent import monkey
monkey.patch_all()

from speedtest_servers import create_app
from config import Config
from gevent import pywsgi

app = create_app(Config)

if __name__ == "__main__":
    gevent_server = pywsgi.WSGIServer(("localhost", 5000), app.wsgi_app)
    gevent_server.serve_forever()
