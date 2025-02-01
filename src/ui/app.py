from flask import Flask, render_template, request, url_for, send_file
from pathlib import Path
from dataclasses import asdict
import yaml
from zipfile import ZipFile
import os.path

from src.read_config.agg_function import AggFunction
from src.read_config.plot import Plot
from src.read_config.get_config import get_config
from src.utilities.dictionary_ops import recursive_index
from src.utilities.paths import (
    config_path,
    spending_path,
    aggregation_path,
    plots_dir,
    static_path,
)
from src.utilities.read_data import read_data

from src.analyze_spending import analyze_spending

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(Path(__file__).parent)


@app.route("/")
@app.route("/home", methods=["GET", "POST"], defaults={"invalid": False})
@app.route("/home/<invalid>")
def home(invalid):
    if request.method == "POST":
        sheet = request.files["file"]
        allowed_extns = {"csv", "txt", "xlsx"}
        if (
            sheet.filename == ""
            or os.path.splitext(sheet.filename)[1] not in allowed_extns
            or not _validate_spending(
                read_data(os.path.join(app.config["UPLOAD_FOLDER"], sheet.filename))
            )
        ):
            return render_template(url_for("home"), invalid=True)

        sheet.save(spending_path())
        analyze_spending()

        zip_path = os.path.join(static_path(), "output.zip")
        with ZipFile(zip_path, "w") as z:
            z.write(aggregation_path())
            plots = Path(plots_dir())
            for subpath in plots.rglob("*"):
                z.write(
                    subpath,
                    arcname=subpath.relative_to(plots),
                )

            send_file(zip_path)

    return render_template("home.html", invalid=invalid)


def _validate_config(config) -> bool:
    raise NotImplementedError


def _validate_spending(spending_df) -> bool:
    raise NotImplementedError


@app.route("/config", methods=["GET", "POST"], defaults={"invalid": False})
@app.route("/config/<invalid>")
def config(invalid):
    config = {
        "globals": get_config()["globals"],
        "plots": {"monthly": {}, "yearly": {}},
        "aggs": {},
    }

    if request.method == "POST":
        for key, val in request.form.items():
            if key != "submit_button" and val != "<DELETED>":
                recursive_index(config, key.split("."), set_to=val)

        config["plots"] = config["plots"]["monthly"] | config["plots"]["yearly"]
        if not _validate_config(config):
            return render_template(url_for("config"), invalid=True)

        with open(config_path(), "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        return render_template(url_for("home"))

    for plt in get_config()["plots"]:
        if plt["timeframe"] == "monthly":
            config["plots"]["monthly"][plt] = asdict(Plot(plt))
        else:
            config["plots"]["yearly"][plt] = asdict(Plot(plt))

    for agg_name, agg in get_config()["aggregations"]:
        config["aggs"][agg_name] = asdict(AggFunction(agg))

    return render_template(
        "config.html",
        monthlys=config["plots"]["monthly"],
        yearlys=config["plots"]["yearly"],
        aggs=config["aggs"],
        invalid=invalid,
    )
