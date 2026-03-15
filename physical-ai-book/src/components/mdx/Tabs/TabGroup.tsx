import React, {useState, useEffect, createContext, useContext} from 'react';
import clsx from 'clsx';
import {useLocation} from '@docusaurus/router';

// Context for tab group state
interface TabGroupContextType {
  selectedValue: string | null;
  setSelectedValue: (value: string) => void;
  groupId: string;
}

const TabGroupContext = createContext<TabGroupContextType | undefined>(undefined);

export interface TabGroupProps {
  groupId: string;              // Unique identifier for state persistence
  persist?: boolean;            // Remember selected tab across sessions
  children: React.ReactNode;    // TabItem children
  className?: string;           // Optional custom styling
  lazy?: boolean;               // Lazy render tabs (only show default initially)
}

export function TabGroup({
  groupId,
  persist = true,
  children,
  className,
  lazy = false,
}: TabGroupProps) {
  const location = useLocation();
  const [selectedValue, setSelectedValue] = useState<string | null>(null);
  const [isClient, setIsClient] = useState(false);

  // Extract tab values from children
  const tabValues = React.Children.map(children, (child) => {
    if (React.isValidElement(child)) {
      return child.props.value;
    }
    return null;
  }).filter(Boolean) as string[];

  // Get default tab (first tab or from URL hash)
  useEffect(() => {
    setIsClient(true);
    
    // Check URL hash first (deep linking)
    const hash = location.hash;
    if (hash && hash.startsWith(`#tab-${groupId}-`)) {
      const hashValue = hash.replace(`#tab-${groupId}-`, '');
      if (tabValues.includes(hashValue)) {
        setSelectedValue(hashValue);
        return;
      }
    }

    // Check localStorage for persisted value
    if (persist && typeof localStorage !== 'undefined') {
      const stored = localStorage.getItem(`tab-${groupId}`);
      if (stored && tabValues.includes(stored)) {
        setSelectedValue(stored);
        return;
      }
    }

    // Default to first tab
    if (tabValues.length > 0) {
      setSelectedValue(tabValues[0]);
    }
  }, [groupId, persist, location.hash, tabValues]);

  // Handle tab selection
  const handleSelect = (value: string) => {
    setSelectedValue(value);
    
    // Persist to localStorage
    if (persist && typeof localStorage !== 'undefined') {
      localStorage.setItem(`tab-${groupId}`, value);
    }

    // Update URL hash for deep linking
    if (typeof window !== 'undefined') {
      const newHash = `#tab-${groupId}-${value}`;
      if (window.location.hash !== newHash) {
        window.history.replaceState(null, '', newHash);
      }
    }
  };

  const contextValue: TabGroupContextType = {
    selectedValue,
    setSelectedValue: handleSelect,
    groupId,
  };

  return (
    <TabGroupContext.Provider value={contextValue}>
      <div
        className={clsx('tabs-container', className)}
        role="tablist"
        aria-label={`Tab group: ${groupId}`}
      >
        {React.Children.map(children, (child, index) => {
          if (React.isValidElement(child)) {
            const isSelected = selectedValue === child.props.value;
            const shouldRender = !lazy || isSelected || selectedValue === null;

            return (
              <div
                role="tabpanel"
                id={`tabpanel-${groupId}-${child.props.value}`}
                aria-labelledby={`tab-${groupId}-${child.props.value}`}
                aria-selected={isSelected}
                hidden={!isSelected}
                className={clsx('tab-panel', {
                  'tab-panel--active': isSelected,
                })}
              >
                {shouldRender && child}
              </div>
            );
          }
          return child;
        })}
      </div>
    </TabGroupContext.Provider>
  );
}

// Hook to use tab group context
export function useTabGroup() {
  const context = useContext(TabGroupContext);
  if (context === undefined) {
    throw new Error('useTabGroup must be used within a TabGroup');
  }
  return context;
}
