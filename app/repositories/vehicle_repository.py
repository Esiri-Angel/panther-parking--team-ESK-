from ..db import get_db


def create(user_id, plate, make, model, color):
    db = get_db()
    cur = db.execute(
        "INSERT INTO vehicle (user_id, plate, make, model, color) VALUES (?, ?, ?, ?, ?)",
        (user_id, plate, make, model, color),
    )
    db.commit()
    return cur.lastrowid


def find_by_plate(plate):
    row = get_db().execute("SELECT * FROM vehicle WHERE plate = ?", (plate,)).fetchone()
    return dict(row) if row else None


def list_for_user(user_id):
    rows = get_db().execute(
        "SELECT * FROM vehicle WHERE user_id = ? ORDER BY plate", (user_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def list_all():
    rows = get_db().execute("SELECT * FROM vehicle ORDER BY id").fetchall()
    return [dict(r) for r in rows]
