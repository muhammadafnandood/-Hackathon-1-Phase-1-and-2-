import React from 'react';
import clsx from 'clsx';

export interface ObjectiveListProps {
  children: React.ReactNode;  // List of objectives (should be <li> elements or text)
  className?: string;         // Optional custom styling
}

export function ObjectiveList({children, className}: ObjectiveListProps) {
  return (
    <div className={clsx('objective-list', className)}>
      <h3 className="objective-list__heading">🎯 Learning Objectives</h3>
      <ul className="objective-list__items">
        {children}
      </ul>
    </div>
  );
}
