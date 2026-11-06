from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..services import permit_service
from ..services.permit_service import PermitError
from .auth import login_required

bp = Blueprint("permits", __name__, url_prefix="/permits")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        try:
            permit_service.request_permit(
                g.user["id"],
                request.form.get("vehicle_id"),
                request.form.get("lot_id"),
            )
            flash("Permit request submitted successfully.")
            return redirect(url_for("permits.index"))
        except PermitError as e:
            flash(str(e))

    return render_template(
        "permits/index.html",
        permits=permit_service.permits_for(g.user["id"]),
        vehicles=permit_service.vehicles_for(g.user["id"]),
        lots=permit_service.available_lots(),
    )
