import {type Dispatch, type SetStateAction} from "react";

interface TimelineSelectableChunkProps {
  mouseDown: boolean;
  selected: boolean;
  setSelected: Dispatch<SetStateAction<boolean>>;
}

const TimelineSelectableChunk = ({ mouseDown, selected, setSelected }: TimelineSelectableChunkProps) => {
  const toggle = () => setSelected(!selected);

  return (
    <div
      className={selected ? "selectable-chunk active" : "selectable-chunk inactive"}
      onClick={toggle}
      onMouseEnter={() => {
        if (mouseDown) toggle();
      }}
      onMouseDown={() => {
        toggle()
      }}
      onClickCapture={() => {
        toggle()
      }}
    />
  );
};

export default TimelineSelectableChunk;
