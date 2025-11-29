# date string has the format ("YYYY-MM-DD HH:MM:SS) using:
# datetime.strptime("2025-11-29 15:30:00", "%Y-%m-%d %H:%M:%S")
# formatted = dt.strftime("%Y-%m-%d %H:%M:%S") for the other way round

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta

from api.domain.wash_booking import WashBooking


def get_connection_or_create_db() -> sqlite3.Connection:
    if not os.path.exists("db"):
        os.mkdir("db")

    connection = sqlite3.connect("washing_times.db")
    cursor = connection.cursor()

    res1 = cursor.execute(
        f"SELECT name "
        f"FROM sqlite_master "
        f"WHERE type='table' AND name='bookings'"
    )

    res2 = cursor.execute(
        f"SELECT name "
        f"FROM sqlite_master "
        f"WHERE type='table' AND name='users'"
    )

    if res1.fetchone() is None or res2.fetchone() is None:
        with open("schema.sql", "r", encoding="utf-8") as f:
            schema = f.read()
            cursor.executescript(schema)

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

def get_booking_from_username(username : str):
    with get_connection() as (_, cursor):
        booking_record = cursor.execute(
            "SELECT * FROM bookings WHERE username = ?",
            (username,)
        ).fetchone()

        return WashBooking(*booking_record)


def create_booking(booking : WashBooking):
    with get_connection() as (_, cursor):
        query = f"""
        INSERT INTO bookings (username, duration, start_time, dry_included)
        VALUES ('{booking.username}', {booking.duration}, 
        '{booking.start_datetime.isoformat()}', {booking.dryIncluded});
        """
        cursor.execute(query)

def get_all_future_bookings():
    with get_connection() as (_, cursor):
        records = cursor.execute(f"SELECT * FROM bookings")
        bookings = [WashBooking(*record) for record in records]
        return [booking for booking in bookings if booking.is_future_booking()]

def get_usernames():
    with get_connection() as (_, cursor):
        records = cursor.execute(f"SELECT username FROM users")
        return [row[0] for row in records]

if __name__ == "__main__":
    print(get_usernames())