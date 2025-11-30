export class UserBooking {
  public username: string
  public startDatetime: Date
  public duration: number

  constructor(username: string, startDatetime: Date, duration: number) {
    this.username = username
    this.startDatetime = startDatetime
    this.duration = duration
  }

  toDto(): UserBookingDTO {
    return new UserBookingDTO(this.username, this.startDatetime.toISOString(), this.duration)
  }
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
    return new UserBooking(this.username, new Date(this.startTimeStr), this.duration)
  }

  static fromJson(json: UserBookingDTO): UserBookingDTO {
    return new UserBookingDTO(json.username, json.startTimeStr, json.duration)
  }
}
