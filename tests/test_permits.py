import pytest

from app.db import get_db


@pytest.fixture
def pending(client, register_and_login):
    register_and_login()
    client.post("/vehicles/", data={
        "plate": "TEST123",
        "make": "Toyota",
        "model": "Camry",
        "color": "Blue",
    })
    client.post("/permits/", data={
        "vehicle_id": "1",
        "lot_id": "1",
    })


@pytest.mark.parametrize("decision", ["approved", "rejected"])
def test_admin_reviews_permit(client, app, pending, decision):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE user SET role = 'admin'")
        db.commit()

    response = client.post("/permits/review", data={
        "permit_id": "1",
        "decision": decision,
    }, follow_redirects=True)

    assert b"Permit decision saved." in response.data
    assert decision.encode() in client.get("/permits/").data

    response = client.post("/permits/review", data={
        "permit_id": "1",
        "decision": "rejected" if decision == "approved" else "approved",
    }, follow_redirects=True)

    assert b"already been reviewed" in response.data

    with app.app_context():
        permit = get_db().execute(
            "SELECT status FROM permit WHERE id = 1"
        ).fetchone()
        assert permit["status"] == decision


def test_driver_cannot_review(client, app, pending):
    assert client.get("/permits/review").status_code == 403

    response = client.post("/permits/review", data={
        "permit_id": "1",
        "decision": "approved",
    })
    assert response.status_code == 403

    with app.app_context():
        permit = get_db().execute(
            "SELECT status FROM permit WHERE id = 1"
        ).fetchone()
        assert permit["status"] == "pending"
