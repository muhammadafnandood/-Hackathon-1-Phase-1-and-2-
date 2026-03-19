import React, { useState, useEffect } from 'react';
import { topicImages, TopicImage } from '../../data/topicImages';

interface AnswerCardData {
  book_answer: string | null;
  extended_knowledge: string;
  mermaid_diagram: string | 'NO_DIAGRAM';
  image_keywords: string[];
}

interface AnswerCardProps {
  data: AnswerCardData;
}

const AnswerCard: React.FC<AnswerCardProps> = ({ data }) => {
  const [diagramSvg, setDiagramSvg] = useState<string>('');
  const [isDiagramLoading, setIsDiagramLoading] = useState(true);
  const [matchedImages, setMatchedImages] = useState<TopicImage[]>([]);

  // Render Mermaid diagram when component mounts
  useEffect(() => {
    if (data.mermaid_diagram && data.mermaid_diagram !== 'NO_DIAGRAM') {
      setIsDiagramLoading(true);
      
      // Load mermaid library dynamically if not already loaded
      const loadMermaid = async () => {
        if (!(window as any).mermaid) {
          const script = document.createElement('script');
          script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
          script.async = true;
          document.head.appendChild(script);
          
          script.onload = () => {
            (window as any).mermaid.initialize({ 
              startOnLoad: false, 
              theme: 'default',
              securityLevel: 'loose',
            });
            renderDiagram();
          };
        } else {
          renderDiagram();
        }
      };

      const renderDiagram = async () => {
        try {
          const id = `mermaid-${Date.now()}`;
          const { svg } = await (window as any).mermaid.render(id, data.mermaid_diagram);
          setDiagramSvg(svg);
        } catch (error) {
          console.error('Mermaid render error:', error);
          setDiagramSvg('<p>Diagram could not be rendered</p>');
        } finally {
          setIsDiagramLoading(false);
        }
      };

      loadMermaid();
    } else {
      setIsDiagramLoading(false);
    }
  }, [data.mermaid_diagram]);

  // Match images based on keywords
  useEffect(() => {
    if (data.image_keywords && data.image_keywords.length > 0) {
      const matched: TopicImage[] = [];
      
      data.image_keywords.forEach((keyword) => {
        const lowerKeyword = keyword.toLowerCase();
        
        // Find matching images
        Object.entries(topicImages).forEach(([topicKey, image]) => {
          const lowerTopic = topicKey.toLowerCase();
          
          // Check if keyword matches topic (partial match)
          if (lowerTopic.includes(lowerKeyword) || lowerKeyword.includes(lowerTopic)) {
            if (!matched.find((m) => m.id === image.id)) {
              matched.push(image);
            }
          }
        });
      });
      
      setMatchedImages(matched.slice(0, 3)); // Limit to 3 images
    }
  }, [data.image_keywords]);

  const formatText = (text: string): React.ReactNode => {
    // Convert markdown-style formatting to HTML
    const formatted = text
      // Bold
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Italic
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Headers with emojis
      .replace(/### 🔧 (.*?)$/gm, '<h4 class="section-header">🔧 $1</h4>')
      .replace(/### 🧩 (.*?)$/gm, '<h4 class="section-header">🧩 $1</h4>')
      .replace(/### ⚡ (.*?)$/gm, '<h4 class="section-header">⚡ $1</h4>')
      .replace(/### 💰 (.*?)$/gm, '<h4 class="section-header">💰 $1</h4>')
      .replace(/### 📚 (.*?)$/gm, '<h4 class="section-header">📚 $1</h4>')
      .replace(/### 🤖 (.*?)$/gm, '<h4 class="section-header robot-header">🤖 $1</h4>')
      // Bullet points
      .replace(/^- (.*?):/gm, '<li><strong>$1:</strong>')
      .replace(/^- (.*?)$/gm, '<li>$1</li>')
      // Price ranges - PKR (Rs.)
      .replace(/Rs\.?\s*([\d,]+(?:\s+(?:lakh|crore))?)?/gi, '<span class="price">Rs. $1</span>')
      .replace(/PKR\s*([\d,]+)/gi, '<span class="price">PKR $1</span>')
      .replace(/(\d+)\s*lakh/gi, '<span class="price">$1 lakh</span>')
      .replace(/(\d+)\s*crore/gi, '<span class="price">$1 crore</span>')
      // Images with styling
      .replace(/!\[(.*?)\]\((.*?)\)/g, '<div class="robot-image-container"><img src="$2" alt="$1" class="robot-image" /><p class="robot-caption">Figure: $1</p></div>')
      // Visual Reference header
      .replace(/\*\*Visual Reference:\*\*/g, '<div class="visual-reference-section">')
      // Italic caption
      .replace(/\*Figure: (.*?)\*/g, '<p class="robot-caption">$1</p>')
      // Line breaks
      .replace(/\n/g, '<br>');
    
    return <div dangerouslySetInnerHTML={{ __html: formatted }} />;
  };

  return (
    <div className="answer-card">
      {/* SECTION A: Book Answer */}
      {data.book_answer ? (
        <div className="card-section book-answer">
          <div className="card-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
            <span>From the Textbook</span>
          </div>
          <div className="card-content">
            {formatText(data.book_answer)}
          </div>
        </div>
      ) : (
        <div className="card-section book-answer not-found">
          <div className="card-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
            <span>From the Textbook</span>
          </div>
          <div className="card-content">
            <p>This topic is not covered in this chapter yet.</p>
          </div>
        </div>
      )}

      {/* SECTION B: Extended AI Knowledge */}
      <div className="card-section extended-knowledge">
        <div className="card-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3M3.343 19.657l.707-.707m15.556 0l-.707-.707M12 21a9 9 0 1 1 0-18 9 9 0 0 1 0 18z"></path>
          </svg>
          <span>Additional Information</span>
        </div>
        <div className="card-content">
          {formatText(data.extended_knowledge)}
        </div>
      </div>

      {/* SECTION C: Architecture Diagram */}
      {data.mermaid_diagram && data.mermaid_diagram !== 'NO_DIAGRAM' && (
        <div className="card-section architecture-diagram">
          <div className="card-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="3" y1="9" x2="21" y2="9"></line>
              <line x1="9" y1="21" x2="9" y2="9"></line>
            </svg>
            <span>Architecture</span>
          </div>
          <div className="card-content diagram-content">
            {isDiagramLoading ? (
              <div className="diagram-loading">
                <div className="skeleton" style={{ height: '200px' }}></div>
                <p>Generating diagram...</p>
              </div>
            ) : (
              <div 
                className="mermaid-diagram"
                dangerouslySetInnerHTML={{ __html: diagramSvg }}
              />
            )}
          </div>
        </div>
      )}

      {/* SECTION D: Visual Guide / Related Images */}
      {matchedImages.length > 0 && (
        <div className="card-section visual-guide">
          <div className="card-header">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <circle cx="8.5" cy="8.5" r="1.5"></circle>
              <polyline points="21 15 16 10 5 21"></polyline>
            </svg>
            <span>Visual Guide</span>
          </div>
          <div className="card-content image-grid">
            {matchedImages.map((image) => (
              <div key={image.id} className="image-item">
                <img 
                  src={image.url} 
                  alt={image.alt} 
                  loading="lazy"
                />
                <p className="image-caption">{image.caption}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Styles */}
      <style>{`
        .answer-card {
          margin-top: 12px;
          display: flex;
          flex-direction: column;
          gap: 12px;
          max-width: 100%; /* Prevent card from overflowing */
          overflow-wrap: break-word; /* Break long words */
        }

        .card-section {
          border-radius: 8px;
          overflow: hidden;
          border: 1px solid;
        }

        .card-header {
          padding: 12px 16px;
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 600;
          font-size: 14px;
          border-bottom: 1px solid;
        }

        .card-header svg {
          flex-shrink: 0;
        }

        .card-content {
          padding: 16px;
          font-size: 14px;
          line-height: 1.6;
        }

        .card-content p {
          margin: 0 0 12px 0;
        }

        .card-content p:last-child {
          margin-bottom: 0;
        }

        .card-content li {
          margin-bottom: 8px;
          margin-left: 20px;
        }

        .card-content .section-header {
          font-size: 15px;
          font-weight: 600;
          margin: 16px 0 10px 0;
          color: var(--ifm-color-primary);
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .card-content .section-header.robot-header {
          color: #424242;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          font-size: 16px;
          margin-top: 20px;
          padding-top: 16px;
          border-top: 2px solid var(--ifm-border-color);
        }

        .card-content .price {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          font-weight: 600;
        }

        /* Robot Image Styles */
        .robot-image-container {
          margin: 20px 0 10px 0;
          padding: 16px;
          background: var(--ifm-background-surface-color);
          border-radius: 12px;
          border: 2px solid var(--ifm-border-color);
          text-align: center;
        }

        .robot-image {
          max-width: 100%;
          max-height: 300px;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          margin: 0 auto;
          display: block;
        }

        .robot-caption {
          margin-top: 12px;
          font-size: 13px;
          color: var(--ifm-font-color-secondary);
          font-style: italic;
          text-align: center;
        }

        .visual-reference-section {
          margin-top: 24px;
          padding-top: 16px;
          border-top: 2px solid var(--ifm-border-color);
        }

        [data-theme='dark'] .card-content .price {
          background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        /* Section A: Book Answer */
        .book-answer {
          background-color: #E8E8E8;
          border-color: #BDBDBD;
          border-left: 3px solid #757575;
        }

        .book-answer .card-header {
          background-color: #DCDCDC;
          border-bottom-color: #BDBDBD;
          color: #212121;
        }

        .book-answer .card-content {
          color: #212121;
        }

        .book-answer.not-found {
          opacity: 0.8;
        }

        .book-answer.not-found .card-content {
          color: #616161;
          font-style: italic;
        }

        [data-theme='dark'] .book-answer {
          background-color: #252525;
          border-color: #3A3A3A;
          border-left-color: #757575;
        }

        [data-theme='dark'] .book-answer .card-header {
          background-color: #1E1E1E;
          border-bottom-color: #3A3A3A;
          color: #E8E8E8;
        }

        [data-theme='dark'] .book-answer .card-content {
          color: #E8E8E8;
        }

        /* Section B: Extended Knowledge */
        .extended-knowledge {
          background-color: #F0F0F0;
          border-color: #BDBDBD;
          border-left: 3px solid #9E9E9E;
        }

        .extended-knowledge .card-header {
          background-color: #E8E8E8;
          border-bottom-color: #BDBDBD;
          color: #212121;
        }

        .extended-knowledge .card-content {
          color: #212121;
        }

        [data-theme='dark'] .extended-knowledge {
          background-color: #2A2A2A;
          border-color: #3A3A3A;
          border-left-color: #9E9E9E;
        }

        [data-theme='dark'] .extended-knowledge .card-header {
          background-color: #242424;
          border-bottom-color: #3A3A3A;
          color: #E8E8E8;
        }

        [data-theme='dark'] .extended-knowledge .card-content {
          color: #E8E8E8;
        }

        /* Section C: Architecture Diagram */
        .architecture-diagram {
          background-color: #E0E0E0;
          border-color: #BDBDBD;
          border-left: 3px solid #616161;
        }

        .architecture-diagram .card-header {
          background-color: #D0D0D0;
          border-bottom-color: #BDBDBD;
          color: #212121;
        }

        .architecture-diagram .card-content {
          background-color: #FFFFFF;
          padding: 16px;
        }

        [data-theme='dark'] .architecture-diagram {
          background-color: #1E1E1E;
          border-color: #3A3A3A;
          border-left-color: #616161;
        }

        [data-theme='dark'] .architecture-diagram .card-header {
          background-color: #181818;
          border-bottom-color: #3A3A3A;
          color: #E8E8E8;
        }

        [data-theme='dark'] .architecture-diagram .card-content {
          background-color: #242424;
        }

        .diagram-content {
          overflow-x: auto;
        }

        .diagram-loading {
          text-align: center;
          padding: 20px;
          color: #616161;
        }

        .diagram-loading p {
          margin-top: 12px;
          font-size: 13px;
        }

        .mermaid-diagram {
          display: flex;
          justify-content: center;
        }

        .mermaid-diagram svg {
          max-width: 100%;
          height: auto;
        }

        /* Section D: Visual Guide */
        .visual-guide {
          background-color: #F5F5F5;
          border-color: #BDBDBD;
          border-left: 3px solid #9E9E9E;
        }

        .visual-guide .card-header {
          background-color: #E8E8E8;
          border-bottom-color: #BDBDBD;
          color: #212121;
        }

        .visual-guide .card-content {
          padding: 16px;
        }

        [data-theme='dark'] .visual-guide {
          background-color: #242424;
          border-color: #3A3A3A;
          border-left-color: #9E9E9E;
        }

        [data-theme='dark'] .visual-guide .card-header {
          background-color: #1E1E1E;
          border-bottom-color: #3A3A3A;
          color: #E8E8E8;
        }

        .image-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 12px;
        }

        .image-item {
          border-radius: 8px;
          overflow: hidden;
          border: 1px solid #DDDDDD;
        }

        [data-theme='dark'] .image-item {
          border-color: #3A3A3A;
        }

        .image-item img {
          width: 100%;
          height: 120px;
          object-fit: cover;
          display: block;
        }

        .image-caption {
          padding: 8px 12px;
          font-size: 12px;
          color: #616161;
          background-color: #FAFAFA;
          margin: 0;
          text-align: center;
        }

        [data-theme='dark'] .image-caption {
          color: #9E9E9E;
          background-color: #1E1E1E;
        }
      `}</style>
    </div>
  );
};

export default AnswerCard;
