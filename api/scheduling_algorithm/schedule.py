
import numpy as np

from api.db.db import get_all_future_bookings
import datetime


# functions:
def get_available_times(chosen_available_times: np.ndarray, stored_wash_start_times: np.ndarray, stored_wash_durations: np.ndarray):
    """
    :param chosen_available_times: array of (start, end) DateTime pairs which the user has indicated they are available for
    :param stored_wash_start_times: array of DateTime values retrieved from the db which indicate already booked slots
    :param stored_wash_durations: array of floats retrieved from the db which indicate duration of each wash in stored_wash_start_times
    :return: array of (start, end) DateTime pairs which can be put into the minimise function to find a time slot.
    """
    ...

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
