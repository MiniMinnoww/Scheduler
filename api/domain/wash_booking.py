from datetime import datetime, timedelta, timezone
import json
# duration is in hours, can be fractional

class WashBooking:
    def __init__(self, id: int | None, username: str, duration: float, start_datetime: datetime):
        self.id = id
        self.username = username
        self.start_datetime = start_datetime
        self.duration = duration


    def get_end_time(self):
        return self.start_datetime + timedelta(hours=self.duration)


    def is_future_booking(self):
        return self.start_datetime > datetime.now(timezone.utc)


    def __str__(self):
        return (
            f"WashBooking(id={self.id}, "
            f"username='{self.username}', "
            f"start_time_str={self.start_datetime.isoformat()}, "
            f"duration={self.duration}"
        )

    def __repr__(self):
        return (
            f"WashBooking(id={self.id!r}, "
            f"username={self.username!r}, "
            f"start_datetime={self.start_datetime!r}, "
            f"duration={self.duration!r}"
        )

    def to_dict(self):
        return {
            "username": self.username,
            "startTimeStr": self.start_datetime.isoformat(),  # convert datetime to string
            "duration": self.duration,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data: dict):
        return WashBooking(id=data["id"],
                           username=data["username"],
                           duration=data["duration"],
                           start_datetime=datetime.fromisoformat(data["start_time"]))

    @staticmethod
    def from_json(json_str: str):
        try:
            data = json.loads(json_str)
            return WashBooking(
                id=None,
                username=str(data["username"]),
                duration=float(data["duration"]),
                start_datetime=datetime.fromisoformat(data["startTimeStr"]))

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        except KeyError as e:
            raise ValueError(f"Missing field in JSON: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid field type or format: {e}")


    def get_occupied_timeslots(self):
        # gets a list of 3 min timeslots it occupies
        timeslots = []
        current = self.start_datetime
        delta = timedelta(minutes=30)

        while current < self.get_end_time():
            timeslots.append(current)
            current += delta

        return timeslots

if __name__ == "__main__":
    booking = WashBooking(1, "alice", 1, datetime.now(timezone.utc))
    print(booking.get_occupied_timeslots())