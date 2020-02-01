from speedtest_servers.views import main

def register_frontend_views(app):
    app.register_blueprint(main.bp)