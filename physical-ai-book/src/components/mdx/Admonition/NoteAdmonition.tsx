import React from 'react';
import clsx from 'clsx';

export interface NoteAdmonitionProps {
  title?: string;             // Optional custom title
  children: React.ReactNode;  // Admonition content
  className?: string;         // Optional custom styling
  icon?: React.ReactNode;     // Optional custom icon
}

export function NoteAdmonition({
  title = 'ℹ️ Note',
  children,
  className,
  icon = 'ℹ️',
}: NoteAdmonitionProps) {
  return (
    <div
      className={clsx('admonition admonition-note', className)}
      role="note"
      aria-label={title}
    >
      <div className="admonition__header">
        <span className="admonition__icon" aria-hidden="true">
          {icon}
        </span>
        <span className="admonition__title">{title}</span>
      </div>
      <div className="admonition__content">
        {children}
      </div>
    </div>
  );
}
