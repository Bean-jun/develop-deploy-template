from app.app import create_app

app = create_app(None)


@app.get("/ping")
def ping():
    from datetime import datetime
    return "pong %s" % datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
