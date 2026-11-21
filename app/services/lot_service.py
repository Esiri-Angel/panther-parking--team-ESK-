
"""Business rules for parking lots."""

from ..repositories import lot_repository

FILLING_THRESHOLD = 0.75  # 75% occupied or more = "filling"


def status_for(capacity, occupied):
    """Return 'open', 'filling' or 'full' for a lot."""
    if occupied >= capacity:
        return "full"
    if occupied / capacity >= FILLING_THRESHOLD:
        return "filling"
    return "open"


def lots_with_status():
    lots = lot_repository.list_all()
    for lot in lots:
        lot["status"] = status_for(lot["capacity"], lot["occupied"])
        lot["available"] = max(lot["capacity"] - lot["occupied"], 0)
    return lots


def validate_lot(name, zone, capacity):
    """Validate parking lot information."""
    errors = []

    if not isinstance(name, str) or not name.strip():
        errors.append("Lot name is required")

    if not isinstance(zone, str) or not zone.strip():
        errors.append("Zone is required")

    try:
        if isinstance(capacity, bool):
            raise ValueError

        if isinstance(capacity, float) and not capacity.is_integer():
            raise ValueError

        capacity = int(capacity)

        if capacity < 1 or capacity > 100000:
            errors.append("Capacity must be between 1 and 100000")

    except (ValueError, TypeError):
        errors.append("Capacity must be a whole number")

    return errors
