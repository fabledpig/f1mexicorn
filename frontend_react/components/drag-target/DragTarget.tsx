import { HTMLAttributes } from 'react';

type Props<T> = Omit<HTMLAttributes<HTMLDivElement>, 'onDrop'> & {
  deserialize: (data: string) => T | undefined;
  onDrop: (data: T) => void;
};

export default function DragTarget<T>({ onDrop, deserialize, ...props }: Props<T>) {
  const onDropInner = (e: React.DragEvent<HTMLDivElement>) => {
    const rawData = atob(e.dataTransfer.getData('text/plain'));
    const data = deserialize(rawData);

    if (data === undefined) {
      return;
    }

    onDrop(data);
  };

  return (
    <div onDragOver={(e) => e.preventDefault()} onDrop={onDropInner} {...props}>
      {props.children}
    </div>
  );
}
