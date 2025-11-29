
import numpy as np

from api.carbonintensityapi.intensity_window import IntensityWindow
from api.db.db import get_all_future_bookings
from datetime import datetime, timedelta

from api.domain.wash_booking import WashBooking


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

def get_best_booking(booking_request: dict) -> WashBooking | None:
    """
    Needs to extract the timings, then cross reference to get the available options
    :param booking_request:
    :return:
    """
    duration = booking_request["duration"]
    valid_windows = get_valid_intensity_windows(booking_request["times"])
    start_time = find_least_intense_slot(valid_windows, duration)
    if start_time is None:
        return Nones
    return WashBooking(None, booking_request["username"], duration, start_time.isoformat())


def find_least_intense_slot(intensity_windows: [IntensityWindow], duration: float) -> datetime | None:
    """
    finds the slot with the lowest average intensity over the duration of the washing
    :param intensity_windows:
    :param duration:
    :return:
    """
    no_slots = int(duration * 2)
    time_score_dict = {}
    for i in range(len(intensity_windows) - no_slots):
        slots = intensity_windows[i:i+no_slots]
        if are_consecutive_slots(slots):
            scores = [slot.forecast for slot in slots]
            time_score_dict[slots[0].time] = np.mean(scores)

    if not time_score_dict:
        return None
    return min(time_score_dict, key=time_score_dict.get)


def are_consecutive_slots(slots: [IntensityWindow]):
    delta = timedelta(minutes=30)
    for i in range(len(slots)-1):
        if slots[i].time + delta != slots[i+1].time:
            return False

    return True

def get_valid_intensity_windows(intensity_windows: [IntensityWindow]):
    return intensity_windows