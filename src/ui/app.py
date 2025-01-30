from flask import Flask, render_template

SITE_TITLE = "Fauxduciary"

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("home.html", site_title=SITE_TITLE)

@app.route("/config")
def config() -> str:
    plots = []
    aggs = []
    return render_template("config.html", plots=plots, aggs=aggs)
