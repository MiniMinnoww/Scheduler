export interface UserBooking {
  username: string
  startDatetime: Date
  duration: number
}

export class UserBookingDTO {
  public username: string
  public startTimeStr: string
  public duration: number

  constructor(username: string, startTimeStr: string, duration: number) {
    this.username = username
    this.startTimeStr = startTimeStr
    this.duration = duration
  }

  toUserBooking(): UserBooking {
    console.log(this.startTimeStr)
    console.log(new Date(this.startTimeStr))
    return {
      username: this.username,
      startDatetime: new Date(this.startTimeStr),
      duration: this.duration
    }
  }
}
