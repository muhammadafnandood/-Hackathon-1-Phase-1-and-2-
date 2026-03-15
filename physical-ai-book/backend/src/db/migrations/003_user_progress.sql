-- Migration: 003_user_progress.sql
-- Description: Create user_progress table for learning progress tracking
-- Created: 2026-03-11

-- User progress table
CREATE TABLE IF NOT EXISTS user_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    chapter_id UUID NOT NULL,
    status VARCHAR(20) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    personalized_mode_used VARCHAR(20),
    time_spent_seconds INTEGER DEFAULT 0,
    completed_at TIMESTAMP WITH TIME ZONE,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, chapter_id)
);

-- Create indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_progress_user_chapter ON user_progress(user_id, chapter_id);
CREATE INDEX IF NOT EXISTS idx_progress_user_status ON user_progress(user_id, status);
CREATE INDEX IF NOT EXISTS idx_progress_completed ON user_progress(completed_at) WHERE completed_at IS NOT NULL;

-- Comment on table
COMMENT ON TABLE user_progress IS 'Learning progress tracking per user per chapter';

-- Comment on columns
COMMENT ON COLUMN user_progress.user_id IS 'Foreign key to users table';
COMMENT ON COLUMN user_progress.chapter_id IS 'Chapter identifier (not foreign key to allow flexibility)';
COMMENT ON COLUMN user_progress.status IS 'Chapter completion status';
COMMENT ON COLUMN user_progress.personalized_mode_used IS 'Last used personalization mode';
COMMENT ON COLUMN user_progress.time_spent_seconds IS 'Total time spent on chapter';
COMMENT ON COLUMN user_progress.completed_at IS 'Completion timestamp';
COMMENT ON COLUMN user_progress.last_accessed_at IS 'Last access timestamp';

-- Create trigger for updated_at (using last_accessed_at)
CREATE TRIGGER update_user_progress_last_accessed
    BEFORE UPDATE ON user_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
