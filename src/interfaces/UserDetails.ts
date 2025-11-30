export class UserDetails {
  public username: string
  public points: number

  constructor(username: string, points: number) {
    this.username = username
    this.points = points
  }

  static fromJson(json: UserDetailsDTO): UserDetails {
    return new UserDetails(json.username, json.points)
  }
}

export class UserDetailsDTO {
  public username: string
  public points: number
}

