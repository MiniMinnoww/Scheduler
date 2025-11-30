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


def score_potential_slots(intensity_windows: [IntensityWindow], duration: float) -> dict | None:
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

    return time_score_dict

def find_least_intense_slot(intensity_windows: [IntensityWindow], duration: float) -> datetime | None:
    time_score_dict = score_potential_slots(intensity_windows, duration)
    if not time_score_dict:
        return None
    return min(time_score_dict, key=time_score_dict.get)

def find_most_intense_slot(intensity_windows: [IntensityWindow], duration: float) -> datetime | None:
    time_score_dict = score_potential_slots(intensity_windows, duration)
    if not time_score_dict:
        return None
    return max(time_score_dict, key=time_score_dict.get)

def are_consecutive_slots(slots: [IntensityWindow]):
    delta = timedelta(minutes=30)
    for i in range(len(slots)-1):
        if slots[i].time + delta != slots[i+1].time:
            return False

    return True

def get_valid_intensity_windows(available_timeslots: list[datetime]) -> list[IntensityWindow]:
    carbon_intensity = CarbonIntensity()
    intensity_windows = carbon_intensity.get_intensity_data_48hrs()
    booked_timeslots = get_booked_timeslots()
    valid_intensity_windows = [window for window in intensity_windows if (window.time not in booked_timeslots) and (window.time in available_timeslots)]

    return valid_intensity_windows

def get_carbon_savings(duration: float) -> int:
    carbon_intensity = CarbonIntensity()
    all_intensity_windows = carbon_intensity.get_intensity_data_48hrs()
    # for now this should only be used to calculate the savings immediately after making a booking
    # since it will only have data for the upcoming 48 hours - idk how to access db in the correct way
    # sort in the morning?
    worst_slot_score = find_most_intense_slot(all_intensity_windows, duration)
    # I have also realised I don't know how to get the actual score we've kept in the dictionary
    # since the functions we've created are returning just a datatime object HELP
    # Oh I give up i don't even know how to refactor the db to store the scores to compare the worst scores to
    return 0

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