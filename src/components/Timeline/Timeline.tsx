import {useEffect, useImperativeHandle, useRef, useState} from "react";
import "../../util/Extensions"
import TimelineChunk, {type TimelineChunkHandle} from "./TimelineChunk.tsx";
import { forwardRef } from "react";
import '../../style/timeline.css';

const MAX_TIME_STEPS: number = 96
const TIME_STEP: number = 0.5 // Half an hour

export interface TimelineHandle {
  getAvailableChunks(): Date[]
}

interface TimelineProps {
  readonly: boolean
  onSelectionChange: (v: boolean[]) => void;
}

const Timeline = forwardRef<TimelineHandle, TimelineProps>(({readonly, onSelectionChange}, ref) => {
  const [times, setTimes] = useState<Date[]>([])
  const [isMouseDown, setIsMouseDown] = useState(false)

  const [selectedChunks, setSelectedChunks] = useState<boolean[]>(() =>
    Array(MAX_TIME_STEPS).fill(false)
  );

  const chunkRefs = useRef<TimelineChunkHandle[]>([]);

  useImperativeHandle(ref, () => ({
    getAvailableChunks: () =>
      times
        .filter((_, i) => selectedChunks[i])
        .map((t) => t)
  }));

  const updateSelection = (index: number, value: boolean) => {
    setSelectedChunks(prev => {
      const updated = [...prev]
      updated[index] = value

      // Call parent with correct data immediately
      onSelectionChange(updated)

      return updated
    })
  }

  useEffect(() => {
    const allHours = []
    for (let i = 0; i < MAX_TIME_STEPS; i++) {
      allHours.push(new Date().ceilToHalfHour().addHours(TIME_STEP * i))
    }
    setTimes(allHours)

    if (readonly) return;

    const handleMouseDown = () => setIsMouseDown(true);
    const handleMouseUp = () => setIsMouseDown(false);

    document.addEventListener("mousedown", handleMouseDown);
    document.addEventListener("mouseup", handleMouseUp);

    return () => {
      document.removeEventListener("mousedown", handleMouseDown);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [readonly])

  return (
    <div className="timeline-container bg-dark text-white">
      {times.map((time, i) => (
        <TimelineChunk
          key={i}
          time={time}
          mouseData={{isMouseDown}}
          readonly={readonly}
          selected={selectedChunks[i]}
          setSelected={(v) => updateSelection(i, v)}
          ref={el => (chunkRefs.current[i] = el!)}
        />
      ))}
    </div>
  )
})


export default Timeline
