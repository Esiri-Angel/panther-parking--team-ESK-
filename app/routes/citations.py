from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from ..services import citation_service
from ..services.citation_service import CitationError
from .auth import login_required

bp = Blueprint("citations", __name__, url_prefix="/citations")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        try:
            citation_service.issue_citation(
                user=g.user,
                plate=request.form.get("plate"),
                lot_id=request.form.get("lot_id"),
                reason=request.form.get("reason"),
                fine_amount=request.form.get("fine_amount"),
            )
            flash("Citation issued successfully.")
            return redirect(url_for("citations.index"))
        except CitationError as e:
            flash(str(e))

    is_admin = g.user.get("role") == "admin"
    if is_admin:
        citations = citation_service.all_citations(g.user)
        lots = citation_service.available_lots()
    else:
        citations = citation_service.citations_for_user(g.user["id"])
        lots = []

    return render_template(
        "citations.html",
        citations=citations,
        lots=lots,
        is_admin=is_admin,
    )

