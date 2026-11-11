DROP TABLE IF EXISTS citation;
DROP TABLE IF EXISTS permit;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS lot;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    role          TEXT    NOT NULL DEFAULT 'driver' CHECK (role IN ('driver', 'admin'))
);

CREATE TABLE lot (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL UNIQUE,
    zone     TEXT    NOT NULL,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    occupied INTEGER NOT NULL DEFAULT 0 CHECK (occupied >= 0)
);

CREATE TABLE vehicle (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (id),
    plate   TEXT    NOT NULL UNIQUE,
    make    TEXT    NOT NULL,
    model   TEXT    NOT NULL,
    color   TEXT    NOT NULL
);

CREATE TABLE permit (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL REFERENCES vehicle (id),
    lot_id     INTEGER NOT NULL REFERENCES lot (id),
    status     TEXT NOT NULL DEFAULT 'pending'
               CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE citation (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    plate       TEXT    NOT NULL,
    lot_id      INTEGER REFERENCES lot (id),
    reason      TEXT    NOT NULL,
    fine_amount REAL    NOT NULL CHECK (fine_amount > 0),
    status      TEXT    NOT NULL DEFAULT 'unpaid'
                CHECK (status IN ('unpaid', 'paid', 'appealed', 'dismissed')),
    issued_by   INTEGER REFERENCES user (id),
    issued_at   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Sample data so the app shows something on first run.
INSERT INTO lot (name, zone, capacity, occupied) VALUES
    ('Lot 1 - Memorial Student Center', 'Student', 220, 40),
    ('Lot 7 - Harrington Science',      'Student', 150, 120),
    ('Lot 12 - Admin Building',         'Faculty/Staff', 80, 80);
