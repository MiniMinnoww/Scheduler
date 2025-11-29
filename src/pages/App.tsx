import 'bootstrap/dist/css/bootstrap.min.css';
import '../style/colors.css';
import '../style/style.css';
import '../style/timeline.css';

import TitleBar from "../components/Titlebar.tsx";
import Timeline, {type TimelineHandle} from "../components/Timeline/Timeline.tsx";
import {useRef} from "react";

function MakeBookingPage() {
  const timelineRef = useRef<TimelineHandle>(null)

  const makeBooking = () => {
    if (!timelineRef.current) return

    fetch("http://localhost:5000/api/send_booking_request", {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        times: timelineRef.current.getAvailableChunks(),
        name: "chArlIe",
        hasDryer: false,
        duration: 1.5
      })
    }).then(res => {
      console.log("Booking made", res);
    });
  }

  return (
    <>
      <TitleBar/>
      <Timeline ref={timelineRef}/>

      <form action={makeBooking}>
        <button type="submit">Make Booking</button>
      </form>

    </>
  )
}

export default MakeBookingPage
