from flask import Flask, render_template, request, url_for, send_file
from pathlib import Path
from zipfile import ZipFile
import os.path

from src.utilities.paths import (
    spending_path,
    aggregation_path,
    plots_dir,
    static_path,
)
from src.utilities.read_data import read_data

from src.analyze_spending import analyze_spending

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(Path(__file__).parent)


def _validate_spending(spending_df) -> bool:
    raise NotImplementedError


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
