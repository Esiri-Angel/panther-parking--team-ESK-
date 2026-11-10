"""Story #7: As an administrator, I want to issue citations to vehicles,
so that campus parking rules and lot regulations are enforced.

Acceptance criteria (one test each):
  AC1 An administrator who submits a valid citation (plate, lot, reason, fine)
      sees the citation in the citations list with status "unpaid".
  AC2 An administrator can issue a citation to an unregistered plate.
  AC3 A submission with an invalid plate, blank reason, non-existent lot, or fine <= 0
      is rejected with a message, and nothing is saved.
  AC4 Only an administrator can issue a citation; a driver or logged-out user cannot.
  AC5 A driver sees citations issued to their registered vehicles, but not other
      drivers' citations.
"""
from werkzeug.security import generate_password_hash

from app.repositories import citation_repository, user_repository


def create_and_login_admin(client, app, email="officer@pvamu.edu", password="adminpassword123"):
    with app.app_context():
        user_repository.create(email, generate_password_hash(password), role="admin")
    return client.post("/auth/login", data={"email": email, "password": password}, follow_redirects=True)


def issue(client, **overrides):
    data = {
        "plate": "PVAMU12",
        "lot_id": "1",
        "reason": "Parked without permit",
        "fine_amount": "50.00",
    }
    data.update(overrides)
    return client.post("/citations/", data=data, follow_redirects=True)


def test_ac1_admin_issues_citation(client, app):
    create_and_login_admin(client, app)
    resp = issue(client, plate="PVAMU12", lot_id="1", reason="Parked without permit", fine_amount="50.00")
    assert b"Citation issued successfully." in resp.data
    assert b"PVAMU12" in resp.data
    assert b"Parked without permit" in resp.data
    assert b"50.00" in resp.data
    assert b"unpaid" in resp.data

    with app.app_context():
        citations = citation_repository.list_all()
        assert len(citations) == 1
        assert citations[0]["plate"] == "PVAMU12"
        assert citations[0]["status"] == "unpaid"
        assert citations[0]["fine_amount"] == 50.00


def test_ac2_citation_for_unregistered_plate(client, app):
    create_and_login_admin(client, app)
    resp = issue(client, plate="UNKNOWN9", lot_id="2", reason="Parked in fire lane", fine_amount="100.00")
    assert b"Citation issued successfully." in resp.data
    assert b"UNKNOWN9" in resp.data
    assert b"Parked in fire lane" in resp.data

    with app.app_context():
        citations = citation_repository.list_by_plate("UNKNOWN9")
        assert len(citations) == 1
        assert citations[0]["reason"] == "Parked in fire lane"
        assert citations[0]["fine_amount"] == 100.00


def test_ac3_invalid_inputs_rejected(client, app):
    create_and_login_admin(client, app)

    # Bad plate - too long
    resp = issue(client, plate="ABCDEFGHI")
    assert b"Plate must be 1 to 8 letters or digits." in resp.data

    # Bad plate - illegal punctuation
    resp = issue(client, plate="AB-123")
    assert b"Plate must be 1 to 8 letters or digits." in resp.data

    # Blank reason
    resp = issue(client, reason="   ")
    assert b"Enter the reason for the citation." in resp.data

    # Zero or negative fine
    resp = issue(client, fine_amount="0")
    assert b"Fine amount must be greater than zero." in resp.data
    resp = issue(client, fine_amount="-25.00")
    assert b"Fine amount must be greater than zero." in resp.data

    # Non-numeric fine
    resp = issue(client, fine_amount="fifty")
    assert b"Enter a valid fine amount." in resp.data

    # Invalid lot id
    resp = issue(client, lot_id="9999")
    assert b"Select a valid parking lot." in resp.data

    # Ensure nothing was saved in the database
    with app.app_context():
        assert citation_repository.list_all() == []


def test_ac4_driver_or_visitor_cannot_issue_citation(client, app, register_and_login):
    # Logged-out visitor attempt
    resp = client.post(
        "/citations/",
        data={"plate": "HACK12", "reason": "No permit", "fine_amount": "50.00"},
    )
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]

    # Regular driver attempt
    register_and_login("driver@pvamu.edu", "password123")
    resp = client.post(
        "/citations/",
        data={"plate": "HACK12", "reason": "No permit", "fine_amount": "50.00"},
        follow_redirects=True,
    )
    assert b"Only administrators can issue citations." in resp.data

    with app.app_context():
        assert citation_repository.list_all() == []


def test_ac5_driver_sees_own_citations_only(client, app, register_and_login):
    # Driver 1 registers vehicle
    register_and_login("driver1@pvamu.edu", "password123")
    client.post("/vehicles/", data={"plate": "DRV1", "make": "Ford", "model": "Focus", "color": "Red"})
    client.get("/auth/logout")

    # Driver 2 registers vehicle
    register_and_login("driver2@pvamu.edu", "password123")
    client.post("/vehicles/", data={"plate": "DRV2", "make": "Honda", "model": "Civic", "color": "Black"})
    client.get("/auth/logout")

    # Admin issues citations to both plates
    create_and_login_admin(client, app)
    issue(client, plate="DRV1", reason="Expired meter", fine_amount="25.00")
    issue(client, plate="DRV2", reason="Blocking driveway", fine_amount="75.00")
    client.get("/auth/logout")

    # Driver 1 logs in and views /citations/
    client.post("/auth/login", data={"email": "driver1@pvamu.edu", "password": "password123"})
    resp1 = client.get("/citations/")
    assert b"DRV1" in resp1.data
    assert b"Expired meter" in resp1.data
    assert b"25.00" in resp1.data
    assert b"DRV2" not in resp1.data
    assert b"Blocking driveway" not in resp1.data
    client.get("/auth/logout")

    # Driver 2 logs in and views /citations/
    client.post("/auth/login", data={"email": "driver2@pvamu.edu", "password": "password123"})
    resp2 = client.get("/citations/")
    assert b"DRV2" in resp2.data
    assert b"Blocking driveway" in resp2.data
    assert b"75.00" in resp2.data
    assert b"DRV1" not in resp2.data
    assert b"Expired meter" not in resp2.data

