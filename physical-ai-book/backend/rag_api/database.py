"""
Database connection and session management
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


class DatabaseSession:
    """Database session manager."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None
    
    def connect(self):
        """Establish database connection."""
        self.conn = psycopg2.connect(self.connection_string)
        return self
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    @contextmanager
    def cursor(self, dict_cursor: bool = True):
        """Context manager for database cursor."""
        cursor = None
        try:
            if dict_cursor:
                cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            else:
                cursor = self.conn.cursor()
            yield cursor
        finally:
            if cursor:
                cursor.close()
    
    def commit(self):
        """Commit transaction."""
        self.conn.commit()
    
    def rollback(self):
        """Rollback transaction."""
        self.conn.rollback()
    
    def execute(self, query: str, params: tuple = None):
        """Execute query and return results."""
        with self.cursor() as cur:
            cur.execute(query, params or ())
            if cur.description:
                return cur.fetchall()
            self.commit()
            return None
    
    def execute_one(self, query: str, params: tuple = None):
        """Execute query and return single result."""
        with self.cursor() as cur:
            cur.execute(query, params or ())
            if cur.description:
                return cur.fetchone()
            self.commit()
            return None


def get_db_session() -> DatabaseSession:
    """Create database session from environment."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    session = DatabaseSession(database_url)
    session.connect()
    return session
