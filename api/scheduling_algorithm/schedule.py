
import numpy as np

from api.db.db import get_all_future_bookings
import datetime

def get_booked_timeslots() -> list[datetime]:
    """
    Gets a list of timeslots that are already occupied
    :return: list of datetime objects
    """
    booked_slots = []
    bookings = get_all_future_bookings()
    for booking in bookings:
        booked_slots.append(*booking.get_occupied_timeslots())

    return booked_slots

def get_best_booking(booking_request: dict):
    """
    Needs to extract the timings, then cross reference to get the available options
    :param booking_request:
    :return:
    """
    ...
