
"""Business rules for permits. No Flask request objects and no SQL here."""

from ..repositories import permit_repository
from ..repositories import vehicle_repository
from ..repositories import lot_repository


class PermitError(Exception):
    """Raised with a user-facing message when a rule is broken."""


def request_permit(user_id, vehicle_id, lot_id):
    if not vehicle_id:
        raise PermitError("Select a vehicle.")

    if not lot_id:
        raise PermitError("Select a parking lot.")

    try:
        vehicle_id = int(vehicle_id)
        lot_id = int(lot_id)
    except (TypeError, ValueError):
        raise PermitError("Invalid vehicle or parking lot.")

    vehicles = vehicle_repository.list_for_user(user_id)

    if not any(v["id"] == vehicle_id for v in vehicles):
        raise PermitError("You can only request permits for your own vehicles.")

    lots = lot_repository.list_all()

    if not any(lot["id"] == lot_id for lot in lots):
        raise PermitError("Select a valid parking lot.")

    return permit_repository.create(vehicle_id, lot_id)


def permits_for(user_id):
    vehicles = vehicle_repository.list_for_user(user_id)
    permits = []

    for vehicle in vehicles:
        permits.extend(
            permit_repository.list_for_vehicle(vehicle["id"])
        )

    return permits


def vehicles_for(user_id):
    return vehicle_repository.list_for_user(user_id)


def available_lots():
    return lot_repository.list_all()
