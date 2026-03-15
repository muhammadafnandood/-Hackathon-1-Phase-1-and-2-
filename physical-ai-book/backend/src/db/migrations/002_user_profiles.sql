-- Migration: 002_user_profiles.sql
-- Description: Create user_profiles table for learning preferences
-- Created: 2026-03-11

-- User profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    programming_level VARCHAR(20) NOT NULL CHECK (programming_level IN ('beginner', 'intermediate', 'advanced')),
    ai_knowledge VARCHAR(20) NOT NULL CHECK (ai_knowledge IN ('none', 'basic', 'intermediate', 'advanced')),
    hardware_availability JSONB NOT NULL DEFAULT '{}',
    learning_pace VARCHAR(20) DEFAULT 'normal' CHECK (learning_pace IN ('slow', 'normal', 'fast')),
    preferred_explanation_style VARCHAR(20) DEFAULT 'both' CHECK (preferred_explanation_style IN ('conceptual', 'practical', 'both')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Create indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_programming ON user_profiles(programming_level);
CREATE INDEX IF NOT EXISTS idx_user_profiles_ai_knowledge ON user_profiles(ai_knowledge);

-- Comment on table
COMMENT ON TABLE user_profiles IS 'Learning profile with preferences and hardware availability';

-- Comment on columns
COMMENT ON COLUMN user_profiles.user_id IS 'Foreign key to users table (one-to-one relationship)';
COMMENT ON COLUMN user_profiles.programming_level IS 'User programming experience level';
COMMENT ON COLUMN user_profiles.ai_knowledge IS 'User AI/ML knowledge level';
COMMENT ON COLUMN user_profiles.hardware_availability IS 'JSONB object with hardware access details';
COMMENT ON COLUMN user_profiles.learning_pace IS 'Preferred learning speed';
COMMENT ON COLUMN user_profiles.preferred_explanation_style IS 'Conceptual vs practical preference';

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
