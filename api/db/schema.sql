CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    duration REAL NOT NULL,
    start_time TEXT NOT NULL,
    dry_included BOOLEAN DEFAULT TRUE
);

INSERT INTO users (username) VALUES
    ('alice'),
    ('bob'),
    ('charlie'),
    ('diana'),
    ('eve'),
    ('frank');
