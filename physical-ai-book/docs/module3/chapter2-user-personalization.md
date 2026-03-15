---
sidebar_label: '2. User Personalization'
---

# Chapter 2: User Personalization & AI Adaptation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERSONALIZED LEARNING SYSTEM                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   User       │────▶│   AI         │────▶│  Personalized│    │
│  │   Profile    │     │   Analyzer   │     │  Content     │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  - Programming Level  - Difficulty Match  - Beginner Mode      │
│  - AI Knowledge     - Pace Adjustment  - Advanced Mode        │
│  - Hardware Access  - Examples Level   - Custom Exercises     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## User Profile Schema

```typescript
interface UserProfile {
  id: string;
  email: string;
  name: string;
  
  // Learning Profile
  programmingLevel: 'beginner' | 'intermediate' | 'advanced';
  aiKnowledge: 'none' | 'basic' | 'intermediate' | 'advanced';
  hardwareAvailability: {
    hasRobot: boolean;
    hasROS2: boolean;
    hasGPU: boolean;
    simulationOnly: boolean;
  };
  
  // Preferences
  learningPace: 'slow' | 'normal' | 'fast';
  preferredExplanationStyle: 'conceptual' | 'practical' | 'both';
  
  // Progress Tracking
  completedChapters: string[];
  currentChapter: string | null;
  personalizedSettings: Record<string, any>;
  
  createdAt: Date;
  updatedAt: Date;
}
```

## Onboarding Flow

### 1. Signup with Profile Questions

```typescript
// pages/signup.tsx
import { useState } from 'react';
import { authClient } from '@/lib/auth';
import { createUserProfile } from '@/lib/api';

export default function SignupPage() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    programmingLevel: 'beginner',
    aiKnowledge: 'none',
    hardwareAvailability: {
      hasRobot: false,
      hasROS2: false,
      hasGPU: false,
      simulationOnly: true,
    },
  });

  const handleSignup = async () => {
    // Step 1: Create auth account
    const { data, error } = await authClient.signUp.email({
      email: formData.email,
      password: formData.password,
      name: formData.name,
    });

    if (error) {
      console.error('Signup failed:', error);
      return;
    }

    // Step 2: Create user profile
    await createUserProfile({
      userId: data.user.id,
      programmingLevel: formData.programmingLevel,
      aiKnowledge: formData.aiKnowledge,
      hardwareAvailability: formData.hardwareAvailability,
    });

    // Redirect to dashboard
    window.location.href = '/dashboard';
  };

  return (
    <div className="onboarding-container">
      {step === 1 && (
        <OnboardingStep1 
          data={formData} 
          onChange={setFormData}
          onNext={() => setStep(2)}
        />
      )}
      
      {step === 2 && (
        <OnboardingStep2 
          data={formData} 
          onChange={setFormData}
          onNext={() => setStep(3)}
        />
      )}
      
      {step === 3 && (
        <OnboardingStep3 
          data={formData} 
          onChange={setFormData}
          onComplete={handleSignup}
        />
      )}
    </div>
  );
}
```

### 2. Onboarding Questions UI

```typescript
// components/onboarding/OnboardingStep2.tsx
export function OnboardingStep2({ data, onChange, onNext }) {
  return (
    <div className="onboarding-step">
      <h2>Tell us about your background</h2>
      
      {/* Programming Level */}
      <div className="question-group">
        <label>What's your programming experience?</label>
        <div className="options">
          <OptionCard
            icon="🌱"
            title="Beginner"
            description="I'm new to programming"
            selected={data.programmingLevel === 'beginner'}
            onClick={() => onChange({ ...data, programmingLevel: 'beginner' })}
          />
          <OptionCard
            icon="🌿"
            title="Intermediate"
            description="I can write basic programs"
            selected={data.programmingLevel === 'intermediate'}
            onClick={() => onChange({ ...data, programmingLevel: 'intermediate' })}
          />
          <OptionCard
            icon="🌳"
            title="Advanced"
            description="I'm comfortable with complex code"
            selected={data.programmingLevel === 'advanced'}
            onClick={() => onChange({ ...data, programmingLevel: 'advanced' })}
          />
        </div>
      </div>

      {/* AI Knowledge */}
      <div className="question-group">
        <label>What's your AI/ML knowledge?</label>
        <div className="options">
          <OptionCard
            icon="🤔"
            title="None"
            description="Never studied AI/ML"
            selected={data.aiKnowledge === 'none'}
            onClick={() => onChange({ ...data, aiKnowledge: 'none' })}
          />
          <OptionCard
            icon="📖"
            title="Basic"
            description="Understand basic concepts"
            selected={data.aiKnowledge === 'basic'}
            onClick={() => onChange({ ...data, aiKnowledge: 'basic' })}
          />
          <OptionCard
            icon="🧠"
            title="Intermediate"
            description="Have built ML models"
            selected={data.aiKnowledge === 'intermediate'}
            onClick={() => onChange({ ...data, aiKnowledge: 'intermediate' })}
          />
          <OptionCard
            icon="🚀"
            title="Advanced"
            description="Work with AI professionally"
            selected={data.aiKnowledge === 'advanced'}
            onClick={() => onChange({ ...data, aiKnowledge: 'advanced' })}
          />
        </div>
      </div>

      <button onClick={onNext}>Next</button>
    </div>
  );
}
```

```typescript
// components/onboarding/OnboardingStep3.tsx
export function OnboardingStep3({ data, onChange, onComplete }) {
  return (
    <div className="onboarding-step">
      <h2>What hardware do you have access to?</h2>
      
      <div className="hardware-options">
        <ToggleOption
          icon="🤖"
          label="Physical Robot"
          description="I have a physical robot to test with"
          checked={data.hardwareAvailability.hasRobot}
          onChange={(checked) => onChange({
            ...data,
            hardwareAvailability: { ...data.hardwareAvailability, hasRobot: checked }
          })}
        />
        
        <ToggleOption
          icon="💻"
          label="ROS2 Installed"
          description="I have ROS2 Humble installed"
          checked={data.hardwareAvailability.hasROS2}
          onChange={(checked) => onChange({
            ...data,
            hardwareAvailability: { ...data.hardwareAvailability, hasROS2: checked }
          })}
        />
        
        <ToggleOption
          icon="🎮"
          label="Simulation Only"
          description="I'll use simulation (Gazebo/Webots)"
          checked={data.hardwareAvailability.simulationOnly}
          onChange={(checked) => onChange({
            ...data,
            hardwareAvailability: { ...data.hardwareAvailability, simulationOnly: checked }
          })}
        />
        
        <ToggleOption
          icon="🖥️"
          label="GPU Available"
          description="I have a GPU for AI training"
          checked={data.hardwareAvailability.hasGPU}
          onChange={(checked) => onChange({
            ...data,
            hardwareAvailability: { ...data.hardwareAvailability, hasGPU: checked }
          })}
        />
      </div>

      <button onClick={onComplete}>Complete Setup</button>
    </div>
  );
}
```

## AI-Powered Chapter Personalization

### Backend API

```typescript
// pages/api/chapters/[chapterId]/personalize.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';
import { getUserProfile } from '@/lib/database';
import { generatePersonalizedContent } from '@/lib/ai';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Get authenticated user
  const session = await auth.api.getSession({ headers: req.headers });
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const { chapterId } = req.query;
  const { mode } = req.body; // 'beginner' | 'advanced' | 'auto'

  // Get user profile
  const userProfile = await getUserProfile(session.user.id);

  // Determine explanation mode
  let explanationMode = mode;
  if (mode === 'auto') {
    explanationMode = userProfile.programmingLevel === 'beginner' 
      ? 'beginner' 
      : 'advanced';
  }

  // Generate personalized content
  const personalizedContent = await generatePersonalizedContent({
    chapterId: chapterId as string,
    userProfile,
    mode: explanationMode,
  });

  res.json({
    success: true,
    content: personalizedContent,
    userProfile,
  });
}
```

### AI Content Generation

```typescript
// lib/ai/personalization.ts
import { ChatOpenAI } from '@langchain/openai';
import { PromptTemplate } from '@langchain/core/prompts';

const llm = new ChatOpenAI({
  modelName: 'gpt-4-turbo',
  temperature: 0.7,
});

const personalizationPrompt = PromptTemplate.fromTemplate(`
You are an educational AI assistant that personalizes technical content based on the learner's background.

## Original Chapter Content:
{chapterContent}

## User Profile:
- Programming Level: {programmingLevel}
- AI Knowledge: {aiKnowledge}
- Hardware Access: {hardwareAvailability}

## Task:
Generate a {mode} explanation of this chapter that:

1. **For Beginner Mode:**
   - Use simple, everyday language
   - Avoid jargon or explain it immediately
   - Use analogies and metaphors
   - Break complex concepts into small steps
   - Provide visual descriptions
   - Include "Why this matters" sections

2. **For Advanced Mode:**
   - Use technical terminology
   - Dive deep into implementation details
   - Include optimization tips
   - Reference advanced patterns
   - Discuss trade-offs and alternatives
   - Link to related advanced topics

Generate the personalized explanation:
`);

export async function generatePersonalizedContent({
  chapterId,
  userProfile,
  mode,
}: {
  chapterId: string;
  userProfile: UserProfile;
  mode: 'beginner' | 'advanced';
}) {
  // Fetch original chapter content
  const chapterContent = await fetchChapterContent(chapterId);

  const prompt = await personalizationPrompt.format({
    chapterContent,
    programmingLevel: userProfile.programmingLevel,
    aiKnowledge: userProfile.aiKnowledge,
    hardwareAvailability: JSON.stringify(userProfile.hardwareAvailability),
    mode,
  });

  const response = await llm.invoke(prompt);

  return {
    chapterId,
    mode,
    personalizedContent: response.content,
    generatedAt: new Date(),
  };
}
```

### Frontend Component

```typescript
// components/chapter/PersonalizeButton.tsx
import { useState } from 'react';
import { useUser } from '@/hooks/useUser';
import { personalizeChapter } from '@/lib/api';

interface PersonalizeButtonProps {
  chapterId: string;
  chapterContent: string;
}

export function PersonalizeButton({ chapterId, chapterContent }: PersonalizeButtonProps) {
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [personalizedContent, setPersonalizedContent] = useState<string | null>(null);
  const [mode, setMode] = useState<'beginner' | 'advanced' | 'auto'>('auto');
  const { user, userProfile } = useUser();

  const handlePersonalize = async () => {
    setIsPersonalizing(true);
    
    try {
      const response = await personalizeChapter(chapterId, mode);
      setPersonalizedContent(response.content.personalizedContent);
    } catch (error) {
      console.error('Personalization failed:', error);
    } finally {
      setIsPersonalizing(false);
    }
  };

  return (
    <div className="personalize-widget">
      <div className="personalize-header">
        <h3>🎯 Personalize This Chapter</h3>
        <p className="description">
          Get AI-generated explanations tailored to your level
        </p>
      </div>

      <div className="mode-selector">
        <button
          className={mode === 'beginner' ? 'active' : ''}
          onClick={() => setMode('beginner')}
        >
          🌱 Beginner
        </button>
        <button
          className={mode === 'auto' ? 'active' : ''}
          onClick={() => setMode('auto')}
        >
          ✨ Auto ({userProfile?.programmingLevel})
        </button>
        <button
          className={mode === 'advanced' ? 'active' : ''}
          onClick={() => setMode('advanced')}
        >
          🚀 Advanced
        </button>
      </div>

      <button
        className="personalize-btn"
        onClick={handlePersonalize}
        disabled={isPersonalizing}
      >
        {isPersonalizing ? '🔄 Generating...' : '✨ Generate Personalized Explanation'}
      </button>

      {personalizedContent && (
        <div className="personalized-content">
          <div className="content-header">
            <h4>Your Personalized Explanation</h4>
            <button onClick={() => setPersonalizedContent(null)}>✕ Close</button>
          </div>
          <div 
            className="markdown-content"
            dangerouslySetInnerHTML={{ __html: personalizedContent }}
          />
        </div>
      )}

      {!personalizedContent && (
        <div className="user-context">
          <p>
            📊 Based on your profile: <strong>{userProfile?.programmingLevel}</strong> programmer,
            AI knowledge: <strong>{userProfile?.aiKnowledge}</strong>
          </p>
        </div>
      )}
    </div>
  );
}
```

### CSS Styling

```css
/* styles/components/personalize-widget.css */
.personalize-widget {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 24px;
  margin: 24px 0;
  color: white;
}

.personalize-header h3 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
}

.personalize-header .description {
  opacity: 0.9;
  font-size: 0.9rem;
  margin: 0;
}

.mode-selector {
  display: flex;
  gap: 12px;
  margin: 20px 0;
}

.mode-selector button {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.mode-selector button.active {
  background: white;
  color: #667eea;
  border-color: white;
}

.mode-selector button:hover:not(.active) {
  background: rgba(255, 255, 255, 0.2);
}

.personalize-btn {
  width: 100%;
  padding: 16px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.personalize-btn:hover:not(:disabled) {
  transform: translateY(-2px);
}

.personalize-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.personalized-content {
  margin-top: 24px;
  background: white;
  color: #333;
  border-radius: 8px;
  padding: 20px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.content-header h4 {
  margin: 0;
  color: #667eea;
}

.content-header button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  opacity: 0.6;
}

.user-context {
  margin-top: 16px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  font-size: 0.9rem;
}

.user-context p {
  margin: 0;
}
```

## Example Personalized Outputs

### Beginner Mode Example

**Original:** "ROS2 nodes communicate via topics using a publish/subscribe model with QoS policies."

**Beginner Explanation:**
> 🌱 **Think of it like YouTube!**
> 
> - **Publisher** = YouTuber uploading videos (sending messages)
> - **Topic** = YouTube channel (the named place where videos go)
> - **Subscriber** = Viewer subscribed to the channel (receiving messages)
> - **QoS** = Video quality settings (reliable = HD, best effort = might buffer)
>
> Just like you don't need to know who's watching your video, publishers don't know who's subscribing. They just send messages to the topic!

### Advanced Mode Example

**Same Original:** "ROS2 nodes communicate via topics using a publish/subscribe model with QoS policies."

**Advanced Explanation:**
> 🚀 **Deep Dive:**
> 
> ROS2's DDS-based pub/sub architecture provides:
> 
> - **Decoupled communication**: Publishers/subscribers are unaware of each other, enabling modular design
> - **QoS Policies**: Configure reliability (RELIABLE vs BEST_EFFORT), durability (TRANSIENT_LOCAL vs VOLATILE), and deadline handling
> - **Zero-copy optimization**: Available with certain DDS implementations for high-throughput scenarios
> - **Discovery**: Automatic participant discovery via RTPS protocol
>
> **Pro Tip:** For real-time control loops, use `BEST_EFFORT` reliability to avoid blocking on late subscribers. For configuration data, use `TRANSIENT_LOCAL` durability so late joiners receive the last message.

## Database Schema

```sql
-- User Profiles Table
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  programming_level VARCHAR(20) NOT NULL,
  ai_knowledge VARCHAR(20) NOT NULL,
  hardware_availability JSONB NOT NULL,
  learning_pace VARCHAR(20) DEFAULT 'normal',
  preferred_explanation_style VARCHAR(20) DEFAULT 'both',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Personalized Content Cache
CREATE TABLE personalized_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  chapter_id VARCHAR(100) NOT NULL,
  mode VARCHAR(20) NOT NULL,
  content TEXT NOT NULL,
  generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, chapter_id, mode)
);

-- Progress Tracking
CREATE TABLE user_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  chapter_id VARCHAR(100) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  personalized_mode_used VARCHAR(20),
  time_spent_seconds INTEGER DEFAULT 0,
  completed_at TIMESTAMP,
  UNIQUE(user_id, chapter_id)
);
```

## Next Steps

- Track user progress through chapters
- Adapt difficulty based on quiz performance
- Recommend next chapters based on profile
- Enable collaborative learning features
