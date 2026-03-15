import React, {useEffect, useRef, useState} from 'react';
import clsx from 'clsx';

export interface MermaidDiagramProps {
  children: string;             // Mermaid diagram definition
  className?: string;           // Optional custom styling
  zoomable?: boolean;           // Enable zoom/pan
  downloadable?: boolean;       // Show download button
}

export function MermaidDiagram({
  children,
  className,
  zoomable = true,
  downloadable = true,
}: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [svgContent, setSvgContent] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [scale, setScale] = useState(1);

  useEffect(() => {
    // Dynamically import mermaid
    const initMermaid = async () => {
      try {
        const mermaid = (await import('mermaid')).default;
        
        await mermaid.initialize({
          startOnLoad: false,
          theme: 'default',
          securityLevel: 'loose',
          fontFamily: 'inherit',
        });

        const {svg} = await mermaid.render('mermaid-svg-' + Math.random().toString(36).substr(2, 9), children);
        setSvgContent(svg);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to render diagram');
      }
    };

    initMermaid();
  }, [children]);

  const handleZoomIn = () => {
    setScale((prev) => Math.min(prev + 0.25, 3));
  };

  const handleZoomOut = () => {
    setScale((prev) => Math.max(prev - 0.25, 0.5));
  };

  const handleReset = () => {
    setScale(1);
  };

  const handleDownload = () => {
    if (!svgContent || !containerRef.current) return;

    const svgBlob = new Blob([svgContent], {type: 'image/svg+xml;charset=utf-8'});
    const url = URL.createObjectURL(svgBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'diagram.svg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  if (error) {
    return (
      <div className={clsx('mermaid-diagram mermaid-diagram--error', className)}>
        <p className="mermaid-diagram__error">❌ {error}</p>
      </div>
    );
  }

  return (
    <div className={clsx('mermaid-diagram', className)} ref={containerRef}>
      {/* Controls */}
      <div className="mermaid-diagram__controls">
        {zoomable && (
          <>
            <button
              className="mermaid-diagram__control"
              onClick={handleZoomIn}
              title="Zoom In"
              aria-label="Zoom in"
            >
              🔍+
            </button>
            <button
              className="mermaid-diagram__control"
              onClick={handleZoomOut}
              title="Zoom Out"
              aria-label="Zoom out"
            >
              🔍-
            </button>
            <button
              className="mermaid-diagram__control"
              onClick={handleReset}
              title="Reset Zoom"
              aria-label="Reset zoom"
            >
              ↺
            </button>
          </>
        )}
        {downloadable && (
          <button
            className="mermaid-diagram__control"
            onClick={handleDownload}
            title="Download SVG"
            aria-label="Download diagram"
          >
            ⬇️ SVG
          </button>
        )}
      </div>

      {/* Diagram */}
      <div
        className="mermaid-diagram__container"
        style={{
          transform: `scale(${scale})`,
          transformOrigin: 'top left',
          overflow: 'auto',
        }}
        dangerouslySetInnerHTML={{__html: svgContent}}
      />
    </div>
  );
}
