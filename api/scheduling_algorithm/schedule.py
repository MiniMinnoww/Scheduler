
from api.carbonintensityapi.intensity_window import IntensityWindow
from api.db.db import get_all_future_bookings
from datetime import datetime, timedelta

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


"""
Need to get booked timeslots
Need to get IntensityWindows
Need to get user available timeslots

From IntensityWindows:
    remove those which are booked
    remove those which are not within the user available timeslots
"""

def get_valid_intensity_windows(available_timeslots: list[datetime]) -> list[IntensityWindow]:
    intensity_windows = [] # replace with Robin's function
    booked_timeslots = get_booked_timeslots()
    valid_intensity_windows = [window for window in intensity_windows if (window.time not in booked_timeslots) and (window.time in available_timeslots)]

    return valid_intensity_windows

if __name__ == '__main__':
    delta = timedelta(minutes=30)
    now = datetime.now()
    windows = [IntensityWindow(now+delta*i, None, None, None) for i in range(10)]