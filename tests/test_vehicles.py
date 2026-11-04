"""Story #2: As a driver, I want to register a vehicle (plate, make, model, color),
so that it can be linked to a permit.

Acceptance criteria (one test each):
  AC1 A logged-in driver who submits a valid plate, make, model and color
      sees the vehicle in their "My vehicles" list at /vehicles/.
  AC2 A plate longer than 8 characters, or with anything other than letters
      and digits, is rejected with a message, and nothing is saved.
  AC3 A plate already registered to another driver (compared case-insensitively)
      is rejected with "This plate is already registered."
  AC4 A submission with a blank make, model or color is rejected with a
      message, and nothing is saved.
  AC5 A driver sees only their own vehicles, and a visitor who is not logged in
      is redirected to the login page.
"""
from app.repositories import vehicle_repository

GOOD = {"plate": "PVAMU12", "make": "Toyota", "model": "Corolla", "color": "Blue"}


def add(client, **overrides):
    return client.post("/vehicles/", data={**GOOD, **overrides}, follow_redirects=True)


def test_ac1_valid_vehicle_appears_in_list(client, register_and_login):
    register_and_login()
    resp = add(client)
    assert b"PVAMU12" in resp.data
    assert b"Toyota" in resp.data
    assert b"Corolla" in resp.data
    assert b"Blue" in resp.data


def test_ac2_bad_plate_rejected(client, app, register_and_login):
    register_and_login()
    too_long = add(client, plate="ABCDEFGHI")  # 9 characters
    assert b"Plate must be" in too_long.data
    bad_chars = add(client, plate="AB-123")
    assert b"Plate must be" in bad_chars.data
    with app.app_context():
        assert vehicle_repository.list_all() == []


def test_ac3_duplicate_plate_rejected(client, app, register_and_login):
    register_and_login("one@pvamu.edu")
    add(client, plate="abc123")
    client.get("/auth/logout")
    register_and_login("two@pvamu.edu")
    resp = add(client, plate="ABC123")  # same plate, different case, different driver
    assert b"This plate is already registered." in resp.data
    with app.app_context():
        assert len(vehicle_repository.list_all()) == 1


def test_ac4_blank_field_rejected(client, app, register_and_login):
    register_and_login()
    for field in ("make", "model", "color"):
        resp = add(client, **{field: "   "})
        assert f"Enter the vehicle {field}.".encode() in resp.data
    with app.app_context():
        assert vehicle_repository.list_all() == []


def test_ac5_only_own_vehicles_and_login_required(client, register_and_login):
    register_and_login("one@pvamu.edu")
    add(client, plate="MINE111")
    client.get("/auth/logout")
    register_and_login("two@pvamu.edu")
    resp = client.get("/vehicles/")
    assert b"MINE111" not in resp.data
    client.get("/auth/logout")
    resp = client.get("/vehicles/")
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]
