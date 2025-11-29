
import numpy as np

# functions:
def get_available_times(chosen_available_times: np.ndarray, stored_wash_start_times: np.ndarray, stored_wash_durations: np.ndarray):
    """
    :param chosen_available_times: array of (start, end) DateTime pairs which the user has indicated they are available for
    :param stored_wash_start_times: array of DateTime values retrieved from the db which indicate already booked slots
    :param stored_wash_durations: array of floats retrieved from the db which indicate duration of each wash in stored_wash_start_times
    :return: array of (start, end) DateTime pairs which can be put into the minimise function to find a time slot.
    """
