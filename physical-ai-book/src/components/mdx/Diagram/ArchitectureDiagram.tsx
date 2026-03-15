import React from 'react';
import clsx from 'clsx';

export interface ArchitectureDiagramProps {
  children: React.ReactNode;    // Diagram content (image or Mermaid)
  title?: string;               // Optional diagram title
  className?: string;           // Optional custom styling
  caption?: string;             // Optional caption
  zoomable?: boolean;           // Enable zoom (for images)
}

export function ArchitectureDiagram({
  children,
  title = 'Architecture Diagram',
  className,
  caption,
  zoomable = true,
}: ArchitectureDiagramProps) {
  return (
    <figure className={clsx('architecture-diagram', className)}>
      {title && <figcaption className="architecture-diagram__title">{title}</figcaption>}
      
      <div className={clsx('architecture-diagram__content', {
        'architecture-diagram__content--zoomable': zoomable,
      })}>
        {children}
      </div>
      
      {caption && (
        <figcaption className="architecture-diagram__caption">
          {caption}
        </figcaption>
      )}
    </figure>
  );
}
