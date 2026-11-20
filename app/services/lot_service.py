"""Business rules for parking lots."""
from ..repositories import lot_repository

FILLING_THRESHOLD = 0.75  # 75% occupied or more = "filling"


def status_for(capacity, occupied):
    """Return 'open', 'filling' or 'full' for a lot.

    Story #5 acceptance criteria live in tests/test_lots.py.
    """
    if occupied >= capacity:
        return "full"
    if occupied / capacity >= FILLING_THRESHOLD:
        return "filling"
    return "open"
    def validate_lot(name, zone, capacity):
    errors = []

    if not name or not name.strip():
        errors.append("Lot name is required")

    if not zone or not zone.strip():
        errors.append("Zone is required")

    try:
        capacity = int(capacity)

        if capacity < 1 or capacity > 100000:
            errors.append("Capacity must be between 1 and 100000")

    except (ValueError, TypeError):
        errors.append("Capacity must be a whole number")

    return errors


def lots_with_status():
    lots = lot_repository.list_all()
    for lot in lots:
        lot["status"] = status_for(lot["capacity"], lot["occupied"])
        lot["available"] = max(lot["capacity"] - lot["occupied"], 0)
    return lots
