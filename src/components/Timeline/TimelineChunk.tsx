import "../../util/Extensions"
import TimelineSelectableChunk from "./TimelineSelectableChunk.tsx";
import {forwardRef, useImperativeHandle, useState} from "react";

interface MouseData {
  isMouseDown: boolean
}

export interface TimelineChunkHandle {
  isSelected(): boolean
  getDate(): Date
}

interface TimelineChunkProps {
  time: Date
  mouseData: MouseData
}

const TimelineChunk = forwardRef<TimelineChunkHandle, TimelineChunkProps>(({time, mouseData}, ref) => {
  const [selected, setSelected] = useState(false)

  useImperativeHandle(ref, () => ({
      isSelected: () => selected,
      getDate: () => time
    }));

  return (
    <div className="timeline-chunk bg-dark">
      <div className="timeline-number bg-dark text-white">
        {time.formatHoursMinutes()}
      </div>

      <TimelineSelectableChunk mouseDown={mouseData.isMouseDown} selected={selected} setSelected={setSelected}/>
    </div>

  )
})

export default TimelineChunk
