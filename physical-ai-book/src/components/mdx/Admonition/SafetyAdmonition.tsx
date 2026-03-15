import React from 'react';
import clsx from 'clsx';

export interface SafetyAdmonitionProps {
  title?: string;             // Optional custom title
  children: React.ReactNode;  // Admonition content
  className?: string;         // Optional custom styling
  icon?: React.ReactNode;     // Optional custom icon
}

export function SafetyAdmonition({
  title = '🛑 Safety Critical',
  children,
  className,
  icon = '🛑',
}: SafetyAdmonitionProps) {
  return (
    <div
      className={clsx('admonition admonition-safety', className)}
      role="alert"
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
