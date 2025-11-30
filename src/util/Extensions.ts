declare global {
  interface Date {
    addHours(h: number): Date;
    ceilToHalfHour(): Date;
    floorToHalfHour(): Date;
    formatHoursMinutes(): string;
  }
}

Date.prototype.addHours = function(hours) {
  this.setTime(this.getTime() + (hours*60*60*1000));
  return this;
}

Date.prototype.ceilToHalfHour = function() {
  this.setMinutes(this.getMinutes() <= 30 ? 30 : 60, 0, 0)
  return this;
}

Date.prototype.floorToHalfHour = function() {
  this.setMinutes(this.getMinutes() <= 30 ? 0 : 30, 0, 0)
  return this;
}

Date.prototype.formatHoursMinutes = function() {
  const hours = this.getHours().toString().padStart(2, "0");
  const minutes = this.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`;
}

export {}