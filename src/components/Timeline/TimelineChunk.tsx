import "../../util/Extensions"
import TimelineSelectableChunk from "./TimelineSelectableChunk.tsx";
import {forwardRef, useImperativeHandle} from "react";

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
  readonly: boolean
  selected: boolean
  setSelected: (b: boolean) => void;
}

const TimelineChunk = forwardRef<TimelineChunkHandle, TimelineChunkProps>(({time, mouseData, readonly, selected, setSelected}, ref) => {

  useImperativeHandle(ref, () => ({
    isSelected: () => selected,
    getDate: () => time
  }));

  return (
    <div className="timeline-chunk bg-dark">
      <div className="timeline-number bg-dark text-white">
        {time.formatHoursMinutes()}
      </div>

      <TimelineSelectableChunk
        mouseDown={mouseData.isMouseDown}
        selected={selected}
        setSelected={v => { setSelected(v); }}
        readonly={readonly}
      />
    </div>
  )
})


export default TimelineChunk
