import React, {useState} from 'react';
import clsx from 'clsx';
import CodeBlock from '@theme/CodeBlock';

export interface CodeCollapsibleProps {
  title?: string;             // Collapsible title
  language?: string;          // Code language for syntax highlighting
  children: React.ReactNode;  // Code content
  defaultOpen?: boolean;      // Initially expanded?
  className?: string;         // Optional custom styling
  showLineNumbers?: boolean;  // Show line numbers
  metastring?: string;        // Code block metastring
}

export function CodeCollapsible({
  title = 'Show Code',
  language = 'python',
  children,
  defaultOpen = false,
  className,
  showLineNumbers = true,
  metastring,
}: CodeCollapsibleProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const toggleOpen = () => {
    setIsOpen(!isOpen);
  };

  // Extract code from children (handle both string and React elements)
  const codeContent = typeof children === 'string' ? children : String(children);

  return (
    <div
      className={clsx('code-collapsible', className, {
        'code-collapsible--open': isOpen,
        'code-collapsible--closed': !isOpen,
      })}
    >
      <button
        className="code-collapsible__header"
        onClick={toggleOpen}
        aria-expanded={isOpen}
      >
        <span className="code-collapsible__icon" aria-hidden="true">
          {isOpen ? '🔽' : '💻'}
        </span>
        <span className="code-collapsible__title">{title}</span>
        <span className="code-collapsible__chevron" aria-hidden="true">
          {isOpen ? '▾' : '▸'}
        </span>
      </button>

      {isOpen && (
        <div className="code-collapsible__content">
          <CodeBlock
            language={language}
            showLineNumbers={showLineNumbers}
            meta={metastring}
          >
            {codeContent}
          </CodeBlock>
        </div>
      )}
    </div>
  );
}
