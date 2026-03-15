import React, {useState} from 'react';
import clsx from 'clsx';

export interface LabBoxProps {
  duration: string;                    // Estimated time (e.g., "45 min")
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  children: React.ReactNode;           // Lab content
  simulationAvailable?: boolean;       // Simulation alternative exists?
  hardwareRequired?: string[];         // Required hardware list
  className?: string;                  // Optional custom styling
  title?: string;                      // Optional custom title
}

export function LabBox({
  duration,
  difficulty,
  children,
  simulationAvailable = true,
  hardwareRequired,
  className,
  title = '🔬 Hands-on Lab',
}: LabBoxProps) {
  const [showHardware, setShowHardware] = useState(false);

  const difficultyColors = {
    beginner: '#10b981',
    intermediate: '#f59e0b',
    advanced: '#ef4444',
  };

  return (
    <div
      className={clsx('lab-box', className, `lab-box--${difficulty}`)}
      role="region"
      aria-label="Hands-on Lab"
    >
      {/* Lab Header */}
      <div className="lab-box__header">
        <h2 className="lab-box__title">{title}</h2>
        <div className="lab-box__badges">
          <span
            className="lab-box__badge lab-box__badge--duration"
            title="Estimated duration"
          >
            ⏱️ {duration}
          </span>
          <span
            className="lab-box__badge lab-box__badge--difficulty"
            style={{backgroundColor: difficultyColors[difficulty]}}
            title="Difficulty level"
          >
            {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
          </span>
        </div>
      </div>

      {/* Hardware Requirements */}
      {hardwareRequired && hardwareRequired.length > 0 && (
        <div className="lab-box__hardware">
          <button
            className="lab-box__hardware-toggle"
            onClick={() => setShowHardware(!showHardware)}
            aria-expanded={showHardware}
          >
            <span className="lab-box__hardware-icon">🛠️</span>
            <span>Hardware Requirements</span>
            <span className="lab-box__chevron">
              {showHardware ? '▾' : '▸'}
            </span>
          </button>

          {showHardware && (
            <ul className="lab-box__hardware-list">
              {hardwareRequired.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          )}

          {simulationAvailable && (
            <p className="lab-box__hardware-note">
              💡 <strong>Simulation Alternative:</strong> Can't access the hardware?
              No problem! Simulation alternatives are provided for each step.
            </p>
          )}
        </div>
      )}

      {/* Lab Content */}
      <div className="lab-box__content">
        {children}
      </div>

      {/* Lab Footer */}
      <div className="lab-box__footer">
        <p className="lab-box__completion">
          ✅ <strong>Completion Checklist:</strong>
        </p>
        <ul className="lab-box__checklist">
          <li>
            <label>
              <input type="checkbox" />
              <span>Understand the core concepts</span>
            </label>
          </li>
          <li>
            <label>
              <input type="checkbox" />
              <span>Complete all code examples</span>
            </label>
          </li>
          <li>
            <label>
              <input type="checkbox" />
              <span>Run the simulation/ hardware test</span>
            </label>
          </li>
          <li>
            <label>
              <input type="checkbox" />
              <span>Document your results</span>
            </label>
          </li>
        </ul>
      </div>
    </div>
  );
}
