
interface TimelineSelectableChunkProps {
  mouseDown: boolean;
  selected: boolean;
  setSelected: (a: boolean) => void;
  readonly: boolean;
}

const TimelineSelectableChunk = ({ mouseDown, selected, setSelected, readonly }: TimelineSelectableChunkProps) => {
  const toggle = () => setSelected(!selected);

  const onclick = () => {
    if (!readonly) toggle()
  }

  const onMouseEnter = () => {
    if (mouseDown && !readonly) toggle();
  }

  const onMouseDown = () => {
    if (!readonly) toggle()
  }

  return (
    <div
      className={selected ? "selectable-chunk active" : "selectable-chunk inactive"}
      onClick={onclick}
      onMouseEnter={onMouseEnter}
      onMouseDown={onMouseDown}
      onClickCapture={onclick}
    />
  );
};

export default TimelineSelectableChunk;
