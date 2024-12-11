import uuid
import psycopg2
import json
from psycopg2.extras import Json, DictCursor
from typing import Optional, Dict, Any

class DatabaseHelper:
    def __init__(self, database: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        """Initialize database connection."""
        self.conn_params = {
            "database": database,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self._create_table()

    def _get_connection(self):
        """Create and return a new database connection."""
        return psycopg2.connect(**self.conn_params)

    def _create_table(self):
        """Create the conversations table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS conversations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            content JSONB NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
            conn.commit()

    def save_conversation(self, content: Dict[str, Any]) -> str:
        """
        Save a new conversation entry to the database.
        
        Args:
            content: Dictionary containing the conversation content, including session_id and role
            
        Returns:
            str: The UUID of the created record
        """
        query = """
        INSERT INTO conversations (content)
        VALUES (%s)
        RETURNING id;
        """
        
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (Json(content),))
                record_id = cur.fetchone()[0]
            conn.commit()
        
        return str(record_id)

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific conversation by its ID.
        
        Args:
            conversation_id: UUID of the conversation to retrieve
            
        Returns:
            Optional[Dict]: Conversation data if found, None otherwise
        """
        query = """
        SELECT id, content, created_at
        FROM conversations
        WHERE id = %s;
        """
        
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, (conversation_id,))
                result = cur.fetchone()
                
        if result:
            return dict(result)
        return None

    def get_conversations_by_session(self, session_id: str) -> list:
        """
        Retrieve all conversations for a specific session.
        
        Args:
            session_id: Session ID to retrieve conversations for
            
        Returns:
            list: List of conversation dictionaries
        """
        query = """
        SELECT id, content, created_at
        FROM conversations
        WHERE content @> %s
        ORDER BY created_at ASC;
        """
        
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, (Json({'session_id': session_id}),))
                results = cur.fetchall()
                
        return [dict(row) for row in results]
