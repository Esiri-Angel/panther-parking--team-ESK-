"""Story #6: As a Parking Office admin, I want to create and edit lots
(name, zone, capacity), so that the system matches campus.

Acceptance criteria:
  AC1 An admin can create a lot with a name, zone and capacity.
  AC2 An admin can edit an existing lot's name, zone and capacity.
  AC3 Name and zone are required, and capacity must be a whole number
      from 1 to 100,000.
  AC4 Lot names must be unique, ignoring upper/lower case.
  AC5 Drivers cannot create or edit lots.
"""
import pytest

from app.services.lot_service import validate_lot


def test_ac1_admin_creates_lot(admin_client):
    data = {"name": "Lot 9 - Science Annex", "zone": "North", "capacity": "120"}
    resp = admin_client.post("/lots/new", data=data, follow_redirects=True)
    assert b"Lot 9 - Science Annex" in resp.data
    assert b"of 120" in resp.data


def test_ac2_admin_edits_lot(admin_client):
    data = {"name": "Lot 1 - Memorial Student Center", "zone": "Central", "capacity": "250"}
    resp = admin_client.post("/lots/1/edit", data=data, follow_redirects=True)
    assert b"of 250" in resp.data


def test_ac3_valid_input():
    assert validate_lot(name="Lot 9", zone="North", capacity=120) == []
    assert validate_lot(name="Lot 9", zone="North", capacity=100000) == []


@pytest.mark.parametrize("name, zone, capacity", [
    ("", "North", 120), ("Lot 9", "", 120), ("Lot 9", "North", 0),
    ("Lot 9", "North", -5), ("Lot 9", "North", 100001), ("Lot 9", "North", "abc"),
])
def test_ac3_invalid_input(name, zone, capacity):
    assert validate_lot(name=name, zone=zone, capacity=capacity) != []


def test_ac4_duplicate_name_rejected(admin_client):
    data = {"name": "LOT 1 - MEMORIAL STUDENT CENTER", "zone": "South", "capacity": "50"}
    admin_client.post("/lots/new", data=data)
    page = admin_client.get("/lots/").data.lower()
    assert page.count(b"lot 1 - memorial student center") == 1


def test_ac5_driver_cannot_create_or_edit(driver_client):
    assert driver_client.get("/lots/new").status_code == 403
    assert driver_client.post("/lots/new", data={"name": "X", "zone": "N", "capacity": "5"}).status_code == 403
    assert driver_client.post("/lots/1/edit", data={"name": "X", "zone": "N", "capacity": "5"}).status_code == 403
