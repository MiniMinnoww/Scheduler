import {useEffect, useImperativeHandle, useRef, useState} from "react";
import "../../util/Extensions"
import TimelineChunk, {type TimelineChunkHandle} from "./TimelineChunk.tsx";
import { forwardRef } from "react";

const MAX_TIME_STEPS: number = 48
const TIME_STEP: number = 0.5 // Half an hour

export interface TimelineHandle {
  getAvailableChunks(): Date[]
}

const Timeline = forwardRef<TimelineHandle, object>((_props, ref) => {
  const [times, setTimes] = useState<Date[]>([])
  const [isMouseDown, setIsMouseDown] = useState(false)

  const chunkRefs = useRef<TimelineChunkHandle[]>([]);

  useImperativeHandle(ref, () => ({
      getAvailableChunks: () => chunkRefs.current.filter((chunk) => chunk.isSelected()).map((chunk) => chunk.getDate())
    }));

  useEffect(() => {
    const allHours = []
    for (let i = 0; i < MAX_TIME_STEPS; i++) {
      allHours.push(new Date().floorToHalfHour().addHours(TIME_STEP * i))
    }

    // eslint-disable-next-line react-hooks/set-state-in-effect
    setTimes(allHours)

    const handleMouseDown = () => setIsMouseDown(true);
    const handleMouseUp = () => setIsMouseDown(false);

    document.addEventListener("mousedown", handleMouseDown);
    document.addEventListener("mouseup", handleMouseUp);

    return () => {
      document.removeEventListener("mousedown", handleMouseDown);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [])

  return (
    <div className="timeline-container bg-dark text-white">
      {times.map((time, i) => (
        <TimelineChunk
          key={time.toLocaleTimeString()}
          time={time}
          mouseData={{"isMouseDown": isMouseDown}}
          ref={el => (chunkRefs.current[i] = el!)}
        />
      ))}
    </div>
  )
})

export default Timeline
