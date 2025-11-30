DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS forecasts;
DROP TABLE IF EXISTS bookings;


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    duration REAL NOT NULL,
    start_time TEXT NOT NULL,
    points FLOAT DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    forecast_time TEXT NOT NULL,
    forecast_value INTEGER NOT NULL,
    actual_value INTEGER,
    index_value TEXT NOT NULL
);

INSERT INTO users (username) VALUES
    ('alice'),
    ('bob'),
    ('charlie'),
    ('diana'),
    ('eve'),
    ('frank');

INSERT INTO bookings (username, duration, start_time, points)
VALUES (
    'charlie',
    1.0,
    '2025-12-01T14:00:00+00:00',
    60.0
);

