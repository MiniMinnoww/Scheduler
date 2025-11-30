import type {UserBooking} from "../interfaces/UserBooking.ts";
import {useEffect} from "react";

interface BookingDisplayProps {
  userBooking: UserBooking | null
}

const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];

function BookingDisplay({userBooking}: BookingDisplayProps) {
  useEffect(() => {
    if (userBooking) console.log(userBooking.startDatetime)
  }, [userBooking]);

  return (
    <div>
      <p>
        You have a booking at&nbsp;
        {userBooking ? userBooking.startDatetime.formatHoursMinutes() : "Unknown"}
        &nbsp;on&nbsp;
        {userBooking ? days[userBooking.startDatetime.getDay()] : "Unknown"}
      </p>
    </div>
  )
}

export default BookingDisplay