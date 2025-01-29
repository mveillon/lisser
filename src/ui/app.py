from flask import Flask, render_template
from pathlib import Path
from os.path import join

TITLE = "Fauxduciary"
ROOT = str(Path(__file__).parent)

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("home.html", title=TITLE)
