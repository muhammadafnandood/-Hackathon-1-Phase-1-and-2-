---
sidebar_label: '3. Urdu Translation & Chatbot'
---

# Chapter 3: Urdu Translation & AI Chatbot

## Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    FINAL PROJECT FLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  User    │───▶│  Reads   │───▶│   Ask    │───▶│   RAG    │  │
│  │  Opens   │    │ Chapter  │    │ Question │    │ Retrieve │  │
│  │  Book    │    │ Content  │    │ (Chat)   │    │ Content  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                              │                   │
│                                              ▼                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │  Urdu    │◀───│  LLM     │◀───│  Vector  │                   │
│  │ Translate │    │  Answer  │    │  Search  │                   │
│  └──────────┘    └──────────┘    └──────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 1. Urdu Translation Feature

### Translation Button Component

```typescript
// components/chapter/UrduTranslateButton.tsx
import { useState } from 'react';
import { translateToUrdu } from '@/lib/translation';

interface UrduTranslateButtonProps {
  chapterContent: string;
  chapterId: string;
}

export function UrduTranslateButton({ chapterContent, chapterId }: UrduTranslateButtonProps) {
  const [isTranslating, setIsTranslating] = useState(false);
  const [urduTranslation, setUrduTranslation] = useState<string | null>(null);
  const [showTranslation, setShowTranslation] = useState(false);

  const handleTranslate = async () => {
    setIsTranslating(true);
    
    try {
      const translated = await translateToUrdu(chapterContent);
      setUrduTranslation(translated);
      setShowTranslation(true);
    } catch (error) {
      console.error('Translation failed:', error);
      alert('Translation failed. Please try again.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className="urdu-translate-widget">
      <button
        className="translate-btn"
        onClick={handleTranslate}
        disabled={isTranslating}
      >
        {isTranslating ? '🔄 Translating...' : '🇵🇰 Translate to Urdu / اردو میں ترجمہ'}
      </button>

      {showTranslation && urduTranslation && (
        <div className="urdu-translation-panel">
          <div className="panel-header">
            <h3>اردو ترجمہ (Urdu Translation)</h3>
            <div className="actions">
              <button onClick={() => setShowTranslation(false)}>✕ Close</button>
              <button onClick={() => navigator.clipboard.writeText(urduTranslation)}>
                📋 Copy
              </button>
            </div>
          </div>
          
          <div 
            className="urdu-content"
            dir="rtl"
            dangerouslySetInnerHTML={{ __html: urduTranslation }}
          />
        </div>
      )}
    </div>
  );
}
```

### Translation API

```typescript
// lib/translation.ts
import { ChatOpenAI } from '@langchain/openai';
import { PromptTemplate } from '@langchain/core/prompts';

const llm = new ChatOpenAI({
  modelName: 'gpt-4-turbo',
  temperature: 0.3,
});

const translationPrompt = PromptTemplate.fromTemplate(`
You are a professional translator who translates technical educational content from English to Urdu.

## Guidelines:
1. Translate accurately while maintaining the original meaning
2. Keep technical terms in English with Urdu explanation in brackets
3. Use simple, clear Urdu that students can understand
4. Preserve code blocks, commands, and technical syntax (do NOT translate these)
5. Maintain formatting (headings, lists, bold/italic)
6. Write Urdu in Nastaliq style using Unicode

## Original Content:
{content}

## Translation Format:
- Keep code blocks in English
- Translate explanations to Urdu
- Add Urdu equivalents for technical terms where common

Translate the following content to Urdu:
`);

export async function translateToUrdu(content: string): Promise<string> {
  const prompt = await translationPrompt.format({ content });
  const response = await llm.invoke(prompt);
  return response.content as string;
}
```

### API Endpoint

```typescript
// pages/api/translate/urdu.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';
import { translateToUrdu } from '@/lib/translation';
import { cacheTranslation } from '@/lib/database';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Verify authentication
  const session = await auth.api.getSession({ headers: req.headers });
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { content, chapterId } = req.body;

  if (!content) {
    return res.status(400).json({ error: 'Content is required' });
  }

  try {
    // Check cache first
    const cached = await getCachedTranslation(chapterId);
    if (cached) {
      return res.json({ translated: cached, fromCache: true });
    }

    // Generate translation
    const translated = await translateToUrdu(content);

    // Cache the translation
    await cacheTranslation(chapterId, translated);

    res.json({ translated, fromCache: false });
  } catch (error) {
    console.error('Translation error:', error);
    res.status(500).json({ error: 'Translation failed' });
  }
}
```

### CSS Styling

```css
/* styles/components/urdu-translate.css */
.urdu-translate-widget {
  margin: 24px 0;
}

.translate-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.translate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4);
}

.translate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.urdu-translation-panel {
  margin-top: 20px;
  background: #f8f9fa;
  border: 2px solid #11998e;
  border-radius: 12px;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #11998e;
  color: white;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.panel-header .actions {
  display: flex;
  gap: 8px;
}

.panel-header button {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: background 0.2s;
}

.panel-header button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.urdu-content {
  padding: 24px;
  font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif;
  font-size: 1.1rem;
  line-height: 2.2;
  direction: rtl;
  text-align: right;
}

.urdu-content code {
  direction: ltr;
  text-align: left;
  display: inline-block;
}

.urdu-content pre {
  direction: ltr;
  text-align: left;
}
```

## 2. AI Chatbot for Chapter Questions

### Chatbot Component

```typescript
// components/chat/ChapterChatbot.tsx
import { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '@/lib/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChapterChatbotProps {
  chapterId: string;
  chapterTitle: string;
}

export function ChapterChatbot({ chapterId, chapterTitle }: ChapterChatbotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault();
    
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage({
        chapterId,
        message: userMessage.content,
        conversationHistory: messages,
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        className="chat-toggle-btn"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '✕ Close Chat' : '💬 Ask Question'}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div className="chat-panel">
          <div className="chat-header">
            <div className="chat-info">
              <h3>💬 Chapter Q&A</h3>
              <p className="chapter-title">{chapterTitle}</p>
            </div>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="empty-state">
                <p>👋 Ask any question about this chapter!</p>
                <p className="examples">
                  Examples:<br/>
                  • "What is a ROS2 node?"<br/>
                  • "Explain publish/subscribe with example"<br/>
                  • "How do I install ROS2?"
                </p>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`message ${msg.role}`}
              >
                <div className="message-avatar">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  {msg.content}
                </div>
                <div className="message-time">
                  {msg.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message assistant loading">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form className="chat-input-form" onSubmit={sendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about this chapter..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !input.trim()}>
              📤
            </button>
          </form>
        </div>
      )}
    </>
  );
}
```

### RAG Chat API

```typescript
// pages/api/chat/rag.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';
import { embedQuery } from '@/lib/embeddings';
import { searchQdrant } from '@/lib/qdrant';
import { generateAnswer } from '@/lib/llm';
import { getUserProfile } from '@/lib/database';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Verify authentication
  const session = await auth.api.getSession({ headers: req.headers });
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { chapterId, message, conversationHistory = [] } = req.body;

  if (!message || !chapterId) {
    return res.status(400).json({ error: 'Message and chapterId required' });
  }

  try {
    // Step 1: Get user profile for personalization
    const userProfile = await getUserProfile(session.user.id);

    // Step 2: Embed the query
    const queryEmbedding = await embedQuery(message);

    // Step 3: Search Qdrant for relevant content
    const searchResults = await searchQdrant({
      embedding: queryEmbedding,
      chapterId,
      topK: 5,
      userId: session.user.id,
    });

    // Step 4: Build context from search results
    const context = searchResults.map(result => ({
      content: result.payload.content,
      source: result.payload.source,
      score: result.score,
    }));

    // Step 5: Generate answer with RAG
    const answer = await generateAnswer({
      query: message,
      context,
      conversationHistory,
      userProfile,
    });

    res.json({
      success: true,
      answer,
      sources: searchResults.map(r => r.payload.source),
    });
  } catch (error) {
    console.error('RAG Chat error:', error);
    res.status(500).json({ error: 'Failed to generate answer' });
  }
}
```

### LLM Answer Generation

```typescript
// lib/llm/answer.ts
import { ChatOpenAI } from '@langchain/openai';
import { PromptTemplate } from '@langchain/core/prompts';

const llm = new ChatOpenAI({
  modelName: 'gpt-4-turbo',
  temperature: 0.7,
});

const ragPrompt = PromptTemplate.fromTemplate(`
You are a helpful AI teaching assistant for a ROS2 Robotics course.

## User Profile:
- Programming Level: {programmingLevel}
- AI Knowledge: {aiKnowledge}

## Conversation History:
{conversationHistory}

## Retrieved Context (from course materials):
{context}

## User Question:
{query}

## Instructions:
1. Answer based on the retrieved context when possible
2. Cite sources (chapter/section) when using context
3. Adjust explanation complexity based on user's profile
4. If context doesn't contain the answer, use your knowledge but mention it
5. Be encouraging and educational
6. For technical terms, provide brief explanations
7. Include code examples when relevant
8. If the question is unrelated to the course, politely redirect

## Answer:
`);

export async function generateAnswer({
  query,
  context,
  conversationHistory,
  userProfile,
}: {
  query: string;
  context: Array<{ content: string; source: string; score: number }>;
  conversationHistory: Array<{ role: string; content: string }>;
  userProfile: { programmingLevel: string; aiKnowledge: string };
}) {
  const contextText = context
    .map((c, i) => `[Source ${i + 1}: ${c.source}]\n${c.content}`)
    .join('\n\n');

  const historyText = conversationHistory
    .slice(-4) // Last 4 messages for context
    .map(m => `${m.role}: ${m.content}`)
    .join('\n');

  const prompt = await ragPrompt.format({
    programmingLevel: userProfile.programmingLevel,
    aiKnowledge: userProfile.aiKnowledge,
    conversationHistory: historyText || 'No previous messages',
    context: contextText,
    query,
  });

  const response = await llm.invoke(prompt);
  return response.content as string;
}
```

### CSS Styling

```css
/* styles/components/chatbot.css */
.chat-toggle-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 1000;
}

.chat-toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(102, 126, 234, 0.5);
}

.chat-panel {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 400px;
  height: 600px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 999;
}

.chat-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.chat-header h3 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
}

.chapter-title {
  margin: 0;
  font-size: 0.85rem;
  opacity: 0.9;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.empty-state .examples {
  margin-top: 16px;
  font-size: 0.85rem;
  color: #888;
  background: white;
  padding: 16px;
  border-radius: 8px;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.message-content {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.5;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.message-time {
  font-size: 0.75rem;
  color: #999;
  margin-top: 4px;
}

.message.user .message-time {
  text-align: right;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: bounce 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-8px);
  }
}

.chat-input-form {
  display: flex;
  gap: 8px;
  padding: 16px;
  background: white;
  border-top: 1px solid #e9ecef;
}

.chat-input-form input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 24px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.chat-input-form input:focus {
  border-color: #667eea;
}

.chat-input-form button {
  width: 48px;
  height: 48px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.chat-input-form button:hover:not(:disabled) {
  transform: scale(1.05);
}

.chat-input-form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

## Complete Chapter Layout

```typescript
// components/chapter/ChapterLayout.tsx
import { UrduTranslateButton } from './UrduTranslateButton';
import { PersonalizeButton } from './PersonalizeButton';
import { ChapterChatbot } from '../chat/ChapterChatbot';

interface ChapterLayoutProps {
  chapterId: string;
  chapterTitle: string;
  chapterContent: string;
  children: React.ReactNode;
}

export function ChapterLayout({
  chapterId,
  chapterTitle,
  chapterContent,
  children,
}: ChapterLayoutProps) {
  return (
    <div className="chapter-page">
      {/* Chapter Header */}
      <header className="chapter-header">
        <h1>{chapterTitle}</h1>
        
        {/* Action Buttons */}
        <div className="chapter-actions">
          <PersonalizeButton
            chapterId={chapterId}
            chapterContent={chapterContent}
          />
          <UrduTranslateButton
            chapterId={chapterId}
            chapterContent={chapterContent}
          />
        </div>
      </header>

      {/* Chapter Content */}
      <article className="chapter-content">
        {children}
      </article>

      {/* Chatbot */}
      <ChapterChatbot
        chapterId={chapterId}
        chapterTitle={chapterTitle}
      />
    </div>
  );
}
```

## Summary

✅ **Urdu Translation**
- Translate chapter content to Urdu
- Preserves code and technical syntax
- RTL layout with proper Urdu fonts

✅ **AI Chatbot**
- Ask questions about chapter content
- RAG retrieves relevant context
- LLM generates personalized answers
- Conversation history support

✅ **Complete Flow**
1. User opens book
2. Reads chapter
3. Clicks "Ask Question"
4. RAG retrieves content from vector DB
5. LLM answers with context
6. Optional: Translate to Urdu
