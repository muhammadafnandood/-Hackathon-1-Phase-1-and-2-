-- Migration: 001_users.sql
-- Description: Create users table (managed by BetterAuth)
-- Created: 2026-03-11

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (BetterAuth managed)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for fast lookup
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Create index on created_at for analytics
CREATE INDEX IF NOT EXISTS idx_users_created ON users(created_at);

-- Comment on table
COMMENT ON TABLE users IS 'Authentication users managed by BetterAuth';

-- Comment on columns
COMMENT ON COLUMN users.id IS 'UUID primary key, referenced by all user-related tables';
COMMENT ON COLUMN users.email IS 'Unique user email, used for authentication';
COMMENT ON COLUMN users.name IS 'User display name';
COMMENT ON COLUMN users.email_verified IS 'Email verification status';
