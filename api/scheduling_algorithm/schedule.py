import numpy as np

from carbon_intensity import CarbonIntensity
from dto.intensity_window import IntensityWindow
from db.db import get_all_future_bookings, create_booking
from datetime import datetime, timedelta, time, timezone
from domain.wash_booking import WashBooking


def get_booked_timeslots() -> list[datetime]:
    """
    Gets a list of timeslots that are already occupied
    :return: list of datetime objects
    """
    booked_slots = []
    bookings = get_all_future_bookings()
    for booking in bookings:
        booked_slots += booking.get_occupied_timeslots()

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
        return None
    return WashBooking(None, booking_request["username"], duration, start_time)


def find_least_intense_slot(intensity_windows: [IntensityWindow], duration: float) -> datetime | None:
    """
    finds the slot with the lowest average intensity over the duration of the washing
    :param intensity_windows:
    :param duration:
    :return:
    """
    num_slots = int(duration * 2)
    time_score_dict = {}
    for i in range(len(intensity_windows) - num_slots+1):
        slots = intensity_windows[i:i+num_slots]
        if are_consecutive_slots(slots):
            scores = [slot.forecast for slot in slots]
            print(slots[0].time, np.mean(scores))
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

"""
Need to get booked timeslots
Need to get IntensityWindows
Need to get user available timeslots

From IntensityWindows:
    remove those which are booked
    remove those which are not within the user available timeslots
"""

def get_valid_intensity_windows(available_timeslots: list[datetime]) -> list[IntensityWindow]:
    carbon_intensity = CarbonIntensity()
    intensity_windows = carbon_intensity.get_intensity_data_48hrs()
    booked_timeslots = get_booked_timeslots()
    valid_intensity_windows = [window for window in intensity_windows if (window.time not in booked_timeslots) and (window.time in available_timeslots)]

    return valid_intensity_windows

if __name__ == '__main__':
    tomorrow = datetime.today().date() + timedelta(days=1)
    time =datetime.combine(
        tomorrow,
        time(18, 30, tzinfo=timezone.utc)
    )

    create_booking(WashBooking(None, 'alice', 0.5,time))

    delta = timedelta(minutes=30)
    print(get_best_booking({
        "username": "alice",
        "times": [time+delta*i for i in range(96)],
        "duration": 1
    }))