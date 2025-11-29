from datetime import datetime, timedelta
import json
# duration is in hours, can be fractional

class WashBooking:
    def __init__(self, id: int, username: str, duration: float, start_time_str: str, dry_included: bool):
        self.id = id
        self.username = username
        self.start_datetime = datetime.fromisoformat(start_time_str)
        self.duration = duration
        self.dryIncluded = dry_included

    def get_end_time(self):
        return self.start_datetime + timedelta(hours=self.duration)

    def get_total_duration(self):
        if self.dryIncluded:
            return self.duration * 2

        return self.duration

    def is_future_booking(self):
        return self.start_datetime > datetime.now()

    def __str__(self):
        return (
            f"WashBooking(id={self.id}, "
            f"username='{self.username}', "
            f"start_time_str={self.start_datetime.isoformat()}, "
            f"duration={self.duration}, "
            f"dryIncluded={self.dryIncluded})"
        )

    def __repr__(self):
        return (
            f"WashBooking(id={self.id!r}, "
            f"username={self.username!r}, "
            f"start_time_str={self.start_datetime!r}, "
            f"duration={self.duration!r}, "
            f"dryIncluded={self.dryIncluded!r})"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "start_time_str": self.start_datetime.isoformat(),  # convert datetime to string
            "duration": self.duration,
            "dryIncluded": self.dryIncluded
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=None,
            username=data["username"],
            duration=data["duration"],
            start_time_str=data["start_time_str"],
            dry_included=data["dryIncluded"]
        )

    @classmethod
    def from_json(cls, json_str: str):
        try:
            data = json.loads(json_str)
            return cls(
                id=int(data["id"]),
                username=str(data["username"]),
                duration=float(data["duration"]),
                start_time_str=data["start_time_str"],
                dry_included=bool(data["dryIncluded"])
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        except KeyError as e:
            raise ValueError(f"Missing field in JSON: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid field type or format: {e}")




