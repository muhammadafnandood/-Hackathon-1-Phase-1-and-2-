-- Neon PostgreSQL Schema for Physical AI Textbook RAG System
-- Database: Neon PostgreSQL (Serverless)

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================
-- Users Table
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User Profile for Personalization
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    programming_experience VARCHAR(50) DEFAULT 'beginner', -- beginner, intermediate, advanced
    ai_experience VARCHAR(50) DEFAULT 'beginner',
    robotics_experience VARCHAR(50) DEFAULT 'beginner',
    hardware_availability VARCHAR(100) DEFAULT 'none', -- none, simulation, jetson, workstation, robot
    gpu_capability VARCHAR(100) DEFAULT 'integrated',
    preferred_language VARCHAR(10) DEFAULT 'en', -- en, ur
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Book Content Tables
-- ============================================
CREATE TABLE IF NOT EXISTS modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id UUID REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    slug VARCHAR(100) NOT NULL,
    content_md TEXT, -- Markdown content
    content_html TEXT, -- Rendered HTML
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(module_id, slug)
);

-- ============================================
-- Chunks for RAG
-- ============================================
CREATE TABLE IF NOT EXISTS chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    heading VARCHAR(255),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_chunks_chapter_id ON chunks(chapter_id);
CREATE INDEX IF NOT EXISTS idx_chunks_heading ON chunks(heading);

-- ============================================
-- Embeddings (using pgvector)
-- ============================================
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id UUID REFERENCES chunks(id) ON DELETE CASCADE,
    embedding vector(1536), -- OpenAI ada-002 dimensions
    model_name VARCHAR(100) DEFAULT 'text-embedding-ada-002',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_embeddings_vector 
ON embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- ============================================
-- Chat History
-- ============================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    session_name VARCHAR(255) DEFAULT 'New Chat',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}', -- Store retrieved chunks, tokens, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for chat history retrieval
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created ON chat_messages(created_at);

-- ============================================
-- User Progress Tracking
-- ============================================
CREATE TABLE IF NOT EXISTS user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'not_started', -- not_started, in_progress, completed
    progress_percent INTEGER DEFAULT 0,
    time_spent_seconds INTEGER DEFAULT 0,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, chapter_id)
);

-- ============================================
-- Urdu Translations
-- ============================================
CREATE TABLE IF NOT EXISTS translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID REFERENCES chapters(id) ON DELETE CASCADE,
    language VARCHAR(10) NOT NULL, -- ur, etc.
    content_md TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- pending, translated, reviewed
    translated_at TIMESTAMP WITH TIME ZONE,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(chapter_id, language)
);

-- ============================================
-- Analytics
-- ============================================
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL, -- page_view, chapter_complete, chat_message, etc.
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for analytics queries
CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON analytics_events(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_event_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_analytics_created ON analytics_events(created_at);

-- ============================================
-- Functions
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chapters_updated_at BEFORE UPDATE ON chapters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Views
-- ============================================

-- View for chapter with module info
CREATE OR REPLACE VIEW v_chapters_with_modules AS
SELECT 
    c.id,
    c.title,
    c.slug,
    c.order_index,
    c.content_md,
    m.title as module_title,
    m.slug as module_slug
FROM chapters c
JOIN modules m ON c.module_id = m.id
ORDER BY m.order_index, c.order_index;

-- View for user progress summary
CREATE OR REPLACE VIEW v_user_progress_summary AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(DISTINCT up.chapter_id) as chapters_accessed,
    COUNT(DISTINCT CASE WHEN up.status = 'completed' THEN up.chapter_id END) as chapters_completed,
    SUM(up.time_spent_seconds) as total_time_seconds
FROM users u
LEFT JOIN user_progress up ON u.id = up.user_id
GROUP BY u.id, u.username;

-- ============================================
-- Initial Data
-- ============================================

-- Insert Module 1
INSERT INTO modules (title, description, order_index, slug) VALUES
('The Robotic Nervous System (ROS 2)', 
 'Learn how robots communicate internally using ROS 2 middleware, nodes, topics, services, and actions',
 1, 'module1')
ON CONFLICT (slug) DO NOTHING;

-- ============================================
-- Grants (for production)
-- ============================================
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO neon_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO neon_user;
