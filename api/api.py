import time
from flask import Flask, request, jsonify
from domain.wash_booking import WashBooking
from db.db import get_all_future_bookings, get_usernames, create_booking
from utlis import *
app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/get-future-bookings')
def get_future_bookings():
    bookings = get_all_future_bookings()
    return {"bookings": [booking.to_json() for booking in bookings]}

@app.route("api/get-user-booking/")
def get_booking_for_user():
    username = request.args.get("username", "")
    if error_dict := validate_username(username):
        return jsonify(error_dict), 400

    return get_booking_for_user(username).to_json()

@app.route("api/save-booking")
def save_booking():
    booking_info = request.get_json()
    try:
        booking = WashBooking.from_json(booking_info)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if booking.username not in get_usernames():
        return jsonify({"error": "Username is not valid."}), 400

    if not booking.is_future_booking():
        return jsonify({"error": "Can only book in the future, not the past."}), 400

    if booking.duration <= 0:
        return jsonify({"error": "Cannot have a negative or 0 duration."}), 400

    create_booking(booking)

@app.route("api/send_available_times")
def format_available_times():
    username = request.args.get("username", "")
    if error_dict:=validate_username(username):
        return jsonify(error_dict), 400
    # send the info to logan i guess after i format the times?
    return {}

if __name__ == "__main__":
    app.run()