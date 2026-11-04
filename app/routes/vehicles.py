from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..services import vehicle_service
from ..services.vehicle_service import VehicleError
from .auth import login_required

bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        try:
            vehicle_service.register(
                g.user["id"],
                request.form.get("plate"),
                request.form.get("make"),
                request.form.get("model"),
                request.form.get("color"),
            )
            flash("Vehicle registered.")
            return redirect(url_for("vehicles.index"))
        except VehicleError as e:
            flash(str(e))
    return render_template("vehicles.html", vehicles=vehicle_service.vehicles_for(g.user["id"]))
