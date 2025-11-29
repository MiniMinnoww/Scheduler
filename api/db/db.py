import sqlite3
from contextlib import contextmanager
import os
from dto.intensity_window import IntensityWindow
from domain.wash_booking import WashBooking


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
DB_PATH = os.path.join(BASE_DIR, "washing_times.db")

def get_connection_or_create_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    res1 = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bookings'"
    ).fetchone()

    res2 = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    ).fetchone()

    res3 = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='forecasts'"
    ).fetchone()

    if res1 is None or res2 is None or res3 is None:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = f.read()
            cursor.executescript(schema)
        connection.commit()

        connection.commit()

    return connection

@contextmanager
def get_connection():
    connection = get_connection_or_create_db()
    # lets you access items by column name so they can be converted into a dict later
    connection.row_factory = sqlite3.Row
    try:
        yield connection, connection.cursor()
    finally:
        if connection:
            connection.commit()
            connection.close()

def get_booking_from_username(username : str) -> WashBooking | None:
    if username not in get_usernames():
        raise ValueError(f"User ({username}) does not exist!")
    with get_connection() as (_, cursor):
        booking_record = cursor.execute(
            "SELECT * FROM bookings WHERE username = ?",
            (username,)
        ).fetchone()

    if booking_record is None:
        return None

    return WashBooking(*booking_record)

def create_booking(booking: WashBooking):
    with get_connection() as (_, cursor):
        query = """
        INSERT INTO bookings (username, duration, start_time)
        VALUES (?, ?, ?);
        """
        cursor.execute(
            query,
            (
                booking.username,
                booking.duration,
                booking.start_datetime.isoformat(),
            )
        )

def get_all_future_bookings():
    with get_connection() as (_, cursor):
        records = cursor.execute(f"SELECT * FROM bookings")
        bookings = [WashBooking.from_dict(dict(record)) for record in records]
        return [booking for booking in bookings if booking.is_future_booking()]

def get_usernames():
    with get_connection() as (_, cursor):
        records = cursor.execute(f"SELECT username FROM users")
        return [row[0].lower() for row in records]

def has_future_booking(username: str):
    with get_connection() as (_, cursor):
        booking = get_booking_from_username(username)

        if booking is None:
            return False

        if booking.is_future_booking():
            return True

        return False

def add_forecasts(forecasts: list[IntensityWindow]):
    with get_connection() as (_, cursor):
        query = """
            INSERT INTO forecasts (forecast_time, forecast_value, actual_value, index_value)
            VALUES (?, ?, ?, ?);
        """
        for forecast in forecasts:
            cursor.execute(
                query,
                (
                    forecast.time.isoformat(),
                    forecast.forecast,
                    forecast.actual,
                    forecast.index,
                )
            )


def get_future_forecasts():
    with get_connection() as (_, cursor):
        records = cursor.execute(f"SELECT * FROM forecasts")
        forecasts = [IntensityWindow.from_db_row(record) for record in records]
        return [forecast for forecast in forecasts if forecast.is_future_forecast()]


if __name__ == "__main__":
    get_booking_from_username("charlie")
