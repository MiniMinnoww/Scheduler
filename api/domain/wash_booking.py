from datetime import datetime, timedelta
import json
# duration is in hours, can be fractional

class WashBooking:
    def __init__(self, id: int, username: str, duration: float, start_time_str: str):
        self.id = id
        self.username = username
        self.start_datetime = datetime.fromisoformat(start_time_str)
        self.duration = duration


    def get_end_time(self):
        return self.start_datetime + timedelta(hours=self.duration)


    def is_future_booking(self):
        return self.start_datetime > datetime.now()

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
            f"start_time_str={self.start_datetime!r}, "
            f"duration={self.duration!r}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "startTimeStr": self.start_datetime.isoformat(),  # convert datetime to string
            "duration": self.duration,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=None,
            username=data["username"],
            duration=data["duration"],
            start_time_str=data["startTimeStr"]
        )

    @classmethod
    def from_json(cls, json_str: str):
        try:
            data = json.loads(json_str)
            return cls(
                id=int(data["id"]),
                username=str(data["username"]),
                duration=float(data["duration"]),
                start_time_str=data["startTimeStr"]
            )
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
    booking = WashBooking(1, "alice", 1, datetime.now().isoformat())
    print(booking.get_occupied_timeslots())