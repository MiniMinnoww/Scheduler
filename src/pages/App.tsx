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
import type {UserBooking} from "../interfaces/UserBooking.tsx";


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

  const onSelectionChange = (selection: boolean[]) =>
    setHasInputtedTimes(selection.some(s => s))

  const usernameRef = useRef<GreetingHandle>(null)


  const sendHasFutureBookingRequest = async () => {
    const res = await fetch(`http://localhost:5000/api/user-has-future-booking?username=${getUsername()}`);
    const json: HasFutureBookingResponse = await res.json();
    setHasBooking(json.result);
    return json.result;
  }

  const getUserFutureBookingRequest =  async () => {
    const res = await fetch(`http://localhost:5000/api/get-user-booking/?username=${getUsername()}`);
    const json: UserBooking = await res.json();
    setUserBooking(json);
  }

  const getUsername = () => usernameRef.current ? usernameRef.current.getUsername() : ""

  useEffect(() => {
    sendHasFutureBookingRequest()
      .then((hasBooking: boolean) => {
        if (hasBooking) getUserFutureBookingRequest()
      })
  }, [usernameRef])

  const confirmBooking = () => {
    // TODO: implement
  }

  const makeBooking = () => {
    if (!timelineRef.current)
      return

    fetch("http://localhost:5000/api/send-booking-request", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        times: timelineRef.current.getAvailableChunks(),
        username: getUsername(),
        duration: 1.5
      })
    }).then(async res => {
      const json: UserBooking = await res.json()
      const ok = confirm(`Booking at ${json.startDatetime.formatHoursMinutes()}`)
      if (ok) confirmBooking()
    })
  }

  return (
    <>
      <TitleBar />
      <Greeting ref={usernameRef}/>

      {hasBooking && <BookingDisplay />}

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
