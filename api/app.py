import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

from api.scheduling_algorithm import schedule
from api.utlis import validate_username
from domain.wash_booking import WashBooking
from db.db import get_all_future_bookings, get_usernames, create_booking, has_future_booking, get_booking_from_username
from datetime import datetime
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # change port if your dev server differs

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/get-future-bookings')
def get_future_bookings():
    bookings = get_all_future_bookings()
    return {"bookings": [booking.to_json() for booking in bookings]}

@app.route("/api/get-user-booking/")
def get_booking_for_user():
    username = request.args.get("username", "")
    if error_dict := validate_username(username):
        return jsonify(error_dict), 400
    try:
        return get_booking_from_username(username).to_json()
    except ValueError as e:
        return jsonify({"error": e}), 400

@app.route("/api/save-booking", methods=["POST"])
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

@app.route("/api/send_booking_request", methods=["POST"])
def process_booking():
    booking_request = json.loads(request.get_json())
    username = booking_request.get("username", "")
    if error_dict:=validate_username(username):
        return jsonify(error_dict), 400

    if (times:=booking_request.get("times", "")) == "":
        return jsonify({"error": "No times were submitted"})

    booking_request["times"] = [datetime.fromisoformat(timeslot) for timeslot in times]

    schedule.get_best_booking(booking_request)


@app.route("/api/user-has-future-booking")
def user_has_future_booking():
    username = request.args.get("username", "")
    if error_dict:= validate_username(username):
        return jsonify(error_dict), 400

    try:
        return {"result":has_future_booking(username)}
    except ValueError as e:
        return jsonify({"error":e}), 400

if __name__ == "__main__":
    app.run()