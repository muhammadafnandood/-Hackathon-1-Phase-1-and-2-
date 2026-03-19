-- Migration 002: Urdu Translations Cache
-- Purpose: Cache Urdu translations to avoid re-translating same chapters
-- Created: 2024

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create urdu_translations table
CREATE TABLE IF NOT EXISTS urdu_translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id VARCHAR(255) UNIQUE NOT NULL,
    urdu_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on chapter_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_urdu_translations_chapter_id 
ON urdu_translations(chapter_id);

-- Create index on created_at for cache management (optional cleanup of old entries)
CREATE INDEX IF NOT EXISTS idx_urdu_translations_created_at 
ON urdu_translations(created_at);

-- Add comment to table
COMMENT ON TABLE urdu_translations IS 
'Cache for Urdu translations of textbook chapters to avoid re-translating';

-- Add comments to columns
COMMENT ON COLUMN urdu_translations.id IS 'Unique identifier for translation entry';
COMMENT ON COLUMN urdu_translations.chapter_id IS 'Unique chapter identifier (e.g., module1/chapter1)';
COMMENT ON COLUMN urdu_translations.urdu_content IS 'Full Urdu translated content in MDX format';
COMMENT ON COLUMN urdu_translations.created_at IS 'Timestamp when translation was created';
COMMENT ON COLUMN urdu_translations.updated_at IS 'Timestamp when translation was last updated';

-- Grant permissions (adjust as needed for your setup)
-- GRANT SELECT, INSERT, UPDATE ON urdu_translations TO your_app_user;

-- Optional: Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Optional: Create trigger to auto-update updated_at
DROP TRIGGER IF EXISTS update_urdu_translations_updated_at ON urdu_translations;
CREATE TRIGGER update_urdu_translations_updated_at
    BEFORE UPDATE ON urdu_translations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Verify table creation
-- \d urdu_translations
