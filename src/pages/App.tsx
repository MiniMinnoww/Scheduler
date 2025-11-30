import 'bootstrap/dist/css/bootstrap.min.css';
import '../style/colors.css';
import '../style/style.css';
import '../style/greeting.css';

import TitleBar from "../components/Titlebar.tsx";
import Timeline, { type TimelineHandle } from "../components/Timeline/Timeline.tsx";
import { useEffect, useRef, useState } from "react";
import Greeting, {type GreetingHandle} from "../components/Greeting.tsx";
import BookingDisplay from "../components/BookingDisplay.tsx";
import MakeBookingButton from "../components/MakeBookingButton.tsx";
import {UserBookingDTO, type UserBooking} from "../interfaces/UserBooking.ts";


interface HasFutureBookingResponse {
  result: boolean
  error: string
}


function App() {
  // Reference to the UI timeline object
  const timelineRef = useRef<TimelineHandle>(null)

  const [hasBooking, setHasBooking] = useState(false)
  const [userBooking, setUserBooking] = useState<UserBooking | null>(null)

  const [hasInputtedTimes, setHasInputtedTimes] = useState(false)
  const [username, setUsername] = useState("charlie")

  const onSelectionChange = (selection: boolean[]) =>
    setHasInputtedTimes(selection.some(s => s))
  

  const sendHasFutureBookingRequest = async () => {
    const res = await fetch(`http://localhost:5000/api/user-has-future-booking?username=${username}`);
    const json: HasFutureBookingResponse = await res.json();
    setHasBooking(json.result);
    return json.result;
  }

  const getUserFutureBookingRequest =  async () => {
    fetch(`http://localhost:5000/api/get-user-booking/?username=${username}`).then(async (res) => {
      const req = await res.json();
      const dto = UserBookingDTO.fromJson(req["booking"])

      setUserBooking(dto.toUserBooking());
    }).catch((error) => {
      alert(`An error occurred!\n${error}`)
    });

  }

  useEffect(() => {
    sendHasFutureBookingRequest()
      .then((hasBooking: boolean) => {
        if (hasBooking) getUserFutureBookingRequest()
        else setUserBooking(null)
      })
  }, [username, userBooking])

  const confirmBooking = (booking: UserBooking) => {
    fetch("http://localhost:5000/api/save-booking", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(booking.toDto())
    }).then(async res => {
      if (!res.ok) {
        const json = await res.json()
        alert(`There was an issue with your booking!\nError code ${res.status}: ${res.statusText}\nError: ${json.error}`)
        return
      }
      else {
        setUserBooking(booking)
      }
    })
  }

  const makeBooking = () => {
    if (!timelineRef.current)
      return

    fetch("http://localhost:5000/api/send-booking-request", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        times: timelineRef.current.getAvailableChunks(),
        username: username,
        duration: 1.5
      })
    }).then(async res => {
      if (!res.ok) {
        alert(`There was an issue with your booking!\nError code ${res.status}: ${res.statusText}`)
        return
      }

      const req = await res.json();
      const dto = UserBookingDTO.fromJson(req["booking"])

      const potentialBooking: UserBooking = dto.toUserBooking()
      const ok = confirm(`Booking at ${potentialBooking.startDatetime.formatHoursMinutes()}`)
      if (ok) confirmBooking(potentialBooking)
    }).catch((reason) => {
      alert(`There was an issue with your booking:\n${reason}`)
    })
  }

  return (
    <>
      <TitleBar />
      <Greeting callback={setUsername}/>

      {hasBooking && <BookingDisplay userBooking={userBooking}/>}

      <Timeline
        ref={timelineRef}
        readonly={hasBooking}
        onSelectionChange={onSelectionChange}
        currentBooking={userBooking}
      />

      {!hasBooking &&
        <MakeBookingButton
          isValidBooking={hasInputtedTimes}
          callback={makeBooking}
        />
      }
    </>
  )
}

export default App
