from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..services import permit_service
from ..services.permit_service import PermitError
from .auth import login_required
from flask import abort

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


@bp.route("/review", methods=("GET", "POST"))
@login_required
def review():
    try:
        pending = permit_service.pending_permits(g.user)
    except PermitError:
        abort(403)

    if request.method == "POST":
        try:
            permit_service.review_permit(
                g.user,
                request.form.get("permit_id"),
                request.form.get("decision"),
            )
            flash("Permit decision saved.")
        except PermitError as e:
            flash(str(e))

        return redirect(url_for("permits.review"))

    return render_template(
        "permit_review.html",
        permits=pending,
    )
