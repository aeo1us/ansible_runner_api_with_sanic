from app import get_app

app = get_app()
if __name__ == '__main__':
    app.run(host=app.config.host, port=app.config.port, workers=app.config.workers, debug=app.config.debug)
