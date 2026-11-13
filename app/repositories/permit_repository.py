
from ..db import get_db


def create(vehicle_id, lot_id):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO permit (vehicle_id, lot_id)
        VALUES (?, ?)
        """,
        (vehicle_id, lot_id),
    )
    db.commit()
    return cur.lastrowid


def find_by_id(permit_id):
    row = get_db().execute(
        "SELECT * FROM permit WHERE id = ?",
        (permit_id,),
    ).fetchone()
    return dict(row) if row else None


def list_all():
    rows = get_db().execute(
        "SELECT * FROM permit ORDER BY id DESC"
    ).fetchall()
    return [dict(row) for row in rows]


def list_for_vehicle(vehicle_id):
    rows = get_db().execute(
        """
        SELECT * FROM permit
        WHERE vehicle_id = ?
        ORDER BY id DESC
        """,
        (vehicle_id,),
    ).fetchall()
    return [dict(row) for row in rows]

def update_status(permit_id, status):

    db = get_db()

    cur = db.execute(

        """

        UPDATE permit

        SET status = ?

        WHERE id = ? AND status = 'pending'

        """,

        (status, permit_id),

    )

    db.commit()

    return cur.rowcount
