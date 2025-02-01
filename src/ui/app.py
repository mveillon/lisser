from flask import Flask, render_template, request, url_for
from dataclasses import asdict
import yaml

from src.read_config.agg_function import AggFunction
from src.read_config.plot import Plot
from src.read_config.get_config import get_config
from src.utilities.dictionary_ops import recursive_index
from src.utilities.paths import config_path

SITE_TITLE = "Fauxduciary"

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", site_title=SITE_TITLE)


@app.route("/config", methods=["GET", "POST"])
def config():
    config = {
        "globals": get_config()["globals"],
        "plots": {"monthly": [], "yearly": []},
        "aggs": {},
    }

    if request.method == "POST":
        for key, val in request.form.items():
            if key != "submit_button" and val != "<DELETED>":
                recursive_index(config, key.split("."), set_to=val)

        with open(config_path(), "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        return render_template(url_for("home"))

    for plt in get_config()["plots"]:
        if plt["timeframe"] == "monthly":
            config["plots"]["monthly"].append(asdict(Plot(plt)))
        else:
            config["plots"]["yearly"].append(asdict(Plot(plt)))

    for agg_name, agg in get_config()["aggregations"]:
        config["aggs"][agg_name] = asdict(AggFunction(agg))

    return render_template(
        "config.html", monthlys=config["plots"]["monthly"], yearlys=config["plots"]["yearly"], aggs=config["aggs"]
    )
