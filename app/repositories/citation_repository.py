from ..db import get_db


def create(plate, lot_id, reason, fine_amount, issued_by=None):
    db = get_db()
    cur = db.execute(
        """
        INSERT INTO citation (plate, lot_id, reason, fine_amount, issued_by)
        VALUES (?, ?, ?, ?, ?)
        """,
        (plate, lot_id, reason, fine_amount, issued_by),
    )
    db.commit()
    return cur.lastrowid


def find_by_id(citation_id):
    row = get_db().execute(
        """
        SELECT c.*, l.name AS lot_name, u.email AS issuer_email
        FROM citation c
        LEFT JOIN lot l ON c.lot_id = l.id
        LEFT JOIN user u ON c.issued_by = u.id
        WHERE c.id = ?
        """,
        (citation_id,),
    ).fetchone()
    return dict(row) if row else None


def list_all():
    rows = get_db().execute(
        """
        SELECT c.*, l.name AS lot_name, u.email AS issuer_email
        FROM citation c
        LEFT JOIN lot l ON c.lot_id = l.id
        LEFT JOIN user u ON c.issued_by = u.id
        ORDER BY c.id DESC
        """
    ).fetchall()
    return [dict(r) for r in rows]


def list_by_plate(plate):
    rows = get_db().execute(
        """
        SELECT c.*, l.name AS lot_name, u.email AS issuer_email
        FROM citation c
        LEFT JOIN lot l ON c.lot_id = l.id
        LEFT JOIN user u ON c.issued_by = u.id
        WHERE UPPER(c.plate) = UPPER(?)
        ORDER BY c.id DESC
        """,
        (plate,),
    ).fetchall()
    return [dict(r) for r in rows]


def list_for_user(user_id):
    rows = get_db().execute(
        """
        SELECT c.*, l.name AS lot_name, u.email AS issuer_email
        FROM citation c
        JOIN vehicle v ON UPPER(c.plate) = UPPER(v.plate)
        LEFT JOIN lot l ON c.lot_id = l.id
        LEFT JOIN user u ON c.issued_by = u.id
        WHERE v.user_id = ?
        ORDER BY c.id DESC
        """,
        (user_id,),
    ).fetchall()
    return [dict(r) for r in rows]

