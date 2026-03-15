import React, {useState, useEffect} from 'react';
import clsx from 'clsx';

export interface CollapsibleSectionProps {
  title: string;                // Section title (visible when collapsed)
  icon?: string | React.ReactNode; // Optional icon
  defaultOpen?: boolean;        // Initially expanded?
  children: React.ReactNode;    // Collapsible content
  className?: string;           // Optional custom styling
  persist?: boolean;            // Remember expanded state
}

export function CollapsibleSection({
  title,
  icon,
  defaultOpen = false,
  children,
  className,
  persist = false,
}: CollapsibleSectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const [isClient, setIsClient] = useState(false);

  // Generate unique ID for persistence
  const sectionId = React.useMemo(() => {
    return `collapsible-${title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}`;
  }, [title]);

  // Restore state from localStorage
  useEffect(() => {
    setIsClient(true);
    if (persist && typeof localStorage !== 'undefined') {
      const stored = localStorage.getItem(sectionId);
      if (stored !== null) {
        setIsOpen(stored === 'true');
      }
    }
  }, [sectionId, persist]);

  // Save state to localStorage
  useEffect(() => {
    if (persist && isClient && typeof localStorage !== 'undefined') {
      localStorage.setItem(sectionId, isOpen.toString());
    }
  }, [isOpen, isClient, persist, sectionId]);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div
      className={clsx('collapsible-section', className, {
        'collapsible-section--open': isOpen,
        'collapsible-section--closed': !isOpen,
      })}
    >
      <button
        className="collapsible-section__header"
        onClick={toggleOpen}
        aria-expanded={isOpen}
        aria-controls={`${sectionId}-content`}
      >
        <span className="collapsible-section__icon" aria-hidden="true">
          {icon || (isOpen ? '🔽' : '▶️')}
        </span>
        <span className="collapsible-section__title">{title}</span>
        <span className="collapsible-section__chevron" aria-hidden="true">
          {isOpen ? '▾' : '▸'}
        </span>
      </button>

      <div
        id={`${sectionId}-content`}
        className={clsx('collapsible-section__content', {
          'collapsible-section__content--open': isOpen,
        })}
        hidden={!isOpen}
      >
        <div className="collapsible-section__body">
          {children}
        </div>
      </div>
    </div>
  );
}
