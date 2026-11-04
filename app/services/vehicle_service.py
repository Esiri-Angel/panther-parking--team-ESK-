"""Business rules for vehicles. No Flask request objects and no SQL here."""
import re

from ..repositories import vehicle_repository

MAX_PLATE_LENGTH = 8
PLATE_PATTERN = re.compile(rf"[A-Za-z0-9]{{1,{MAX_PLATE_LENGTH}}}")


class VehicleError(Exception):
    """Raised with a user-facing message when a rule is broken."""


def register(user_id, plate, make, model, color):
    plate = (plate or "").strip().upper()
    if not PLATE_PATTERN.fullmatch(plate):
        raise VehicleError(f"Plate must be 1 to {MAX_PLATE_LENGTH} letters or digits.")
    fields = {"make": make, "model": model, "color": color}
    cleaned = {}
    for name, value in fields.items():
        cleaned[name] = (value or "").strip()
        if not cleaned[name]:
            raise VehicleError(f"Enter the vehicle {name}.")
    if vehicle_repository.find_by_plate(plate):
        raise VehicleError("This plate is already registered.")
    return vehicle_repository.create(user_id, plate, **cleaned)


def vehicles_for(user_id):
    return vehicle_repository.list_for_user(user_id)
