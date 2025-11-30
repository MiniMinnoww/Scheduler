export class UserBooking {
  public username: string
  public startDatetime: Date
  public duration: number
  public points: number

  constructor(username: string, startDatetime: Date, duration: number, points: number) {
    this.username = username
    this.startDatetime = startDatetime
    this.duration = duration
    this.points = points
  }

  toDto(): UserBookingDTO {
    return new UserBookingDTO(this.username, this.startDatetime.toISOString(), this.duration, this.points)
  }
}

export class UserBookingDTO {
  public username: string
  public startTimeStr: string
  public duration: number
  public points: number

  constructor(username: string, startTimeStr: string, duration: number, points: number) {
    this.username = username
    this.startTimeStr = startTimeStr
    this.duration = duration
    this.points = points
  }

  toUserBooking(): UserBooking {
    return new UserBooking(this.username, new Date(this.startTimeStr), this.duration, this.points)
  }

  static fromJson(json: UserBookingDTO): UserBookingDTO {
    return new UserBookingDTO(json.username, json.startTimeStr, json.duration, json.points)
  }
}
