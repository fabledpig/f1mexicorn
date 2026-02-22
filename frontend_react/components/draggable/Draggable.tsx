import { HTMLAttributes, memo } from 'react';

type Props = Omit<HTMLAttributes<HTMLDivElement>, 'draggable'> & {
  serialize: () => string;
};

export default memo(function Draggable({ serialize, ...props }: Props) {
  const onDragStart = (event: React.DragEvent<HTMLDivElement>) => {
    const data = btoa(serialize());
    event.dataTransfer.setData('text/plain', data);
  };

  return (
    <div draggable={true} onDragStart={onDragStart} {...props}>
      {props.children}
    </div>
  );
});
