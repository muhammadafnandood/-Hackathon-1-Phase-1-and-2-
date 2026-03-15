import React from 'react';
import clsx from 'clsx';
import {useTabGroup} from './TabGroup';

export interface TabItemProps {
  value: string;                // Tab identifier
  label: string;                // Display label
  icon?: string | React.ReactNode; // Optional icon
  children: React.ReactNode;    // Tab content
  className?: string;           // Optional custom styling
  attributes?: Record<string, string>; // Extra HTML attributes
}

export function TabItem({
  value,
  label,
  icon,
  children,
  className,
  attributes = {},
}: TabItemProps) {
  const context = useTabGroup();
  const isSelected = context.selectedValue === value;

  const handleClick = () => {
    context.setSelectedValue(value);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  return (
    <>
      {/* Tab Button */}
      <button
        id={`tab-${context.groupId}-${value}`}
        role="tab"
        aria-selected={isSelected}
        aria-controls={`tabpanel-${context.groupId}-${value}`}
        tabIndex={isSelected ? 0 : -1}
        className={clsx(
          'tabs__item',
          className,
          {
            'tabs__item--active': isSelected,
          }
        )}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        {...attributes}
      >
        {icon && (
          <span className="tabs__item-icon" aria-hidden="true">
            {typeof icon === 'string' ? icon : icon}
          </span>
        )}
        <span className="tabs__item-label">{label}</span>
      </button>

      {/* Tab Content (rendered by TabGroup) */}
      <div
        className={clsx('tabs__content', {
          'tabs__content--active': isSelected,
        })}
        hidden={!isSelected}
      >
        {children}
      </div>
    </>
  );
}
