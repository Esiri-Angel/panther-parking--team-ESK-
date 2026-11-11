"""Business rules for citations. No Flask request objects and no SQL here."""
import re

from ..repositories import citation_repository, lot_repository

MAX_PLATE_LENGTH = 8
PLATE_PATTERN = re.compile(rf"[A-Za-z0-9]{{1,{MAX_PLATE_LENGTH}}}")


class CitationError(Exception):
    """Raised with a user-facing message when a rule is broken."""


def issue_citation(user, plate, lot_id, reason, fine_amount):
    """Enforce rules for issuing a parking citation.

    Only administrators may issue citations.
    """
    if not user or user.get("role") != "admin":
        raise CitationError("Only administrators can issue citations.")

    plate = (plate or "").strip().upper()
    if not PLATE_PATTERN.fullmatch(plate):
        raise CitationError(f"Plate must be 1 to {MAX_PLATE_LENGTH} letters or digits.")

    reason = (reason or "").strip()
    if not reason:
        raise CitationError("Enter the reason for the citation.")

    try:
        fine = float(fine_amount)
    except (TypeError, ValueError):
        raise CitationError("Enter a valid fine amount.")

    if fine <= 0:
        raise CitationError("Fine amount must be greater than zero.")

    validated_lot_id = None
    if lot_id is not None and str(lot_id).strip() != "":
        try:
            validated_lot_id = int(lot_id)
        except (TypeError, ValueError):
            raise CitationError("Invalid parking lot selected.")

        lots = lot_repository.list_all()
        if not any(lot["id"] == validated_lot_id for lot in lots):
            raise CitationError("Select a valid parking lot.")

    citation_id = citation_repository.create(
        plate=plate,
        lot_id=validated_lot_id,
        reason=reason,
        fine_amount=round(fine, 2),
        issued_by=user.get("id"),
    )
    return citation_repository.find_by_id(citation_id)


def citations_for_user(user_id):
    """Return all citations matching vehicles registered to the given user."""
    return citation_repository.list_for_user(user_id)


def all_citations(user):
    """Return all citations. Requires admin role."""
    if not user or user.get("role") != "admin":
        raise CitationError("Only administrators can view all citations.")
    return citation_repository.list_all()


def available_lots():
    """Return all parking lots for selection."""
    return lot_repository.list_all()

