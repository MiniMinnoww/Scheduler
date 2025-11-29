interface MakeBookingButtonProps {
  isValidBooking: boolean;
  callback: () => void;
}

function MakeBookingButton({isValidBooking, callback}: MakeBookingButtonProps) {
  return (
    <button
      type="submit"
      className={isValidBooking ? "btn btn-success" : "btn btn-danger"}
      disabled={!isValidBooking}
      onClick={callback}>
    Make Booking
    </button>
  )
}

export default MakeBookingButton