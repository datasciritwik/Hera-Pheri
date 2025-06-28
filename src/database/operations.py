import uuid
import json
from typing import List, Dict, Any

# Import the connection manager from the local package.
from src.database.connection import get_db_connection

def create_conversation_id() -> str:
    """Generates a unique ID for a new conversation run."""
    return uuid.uuid4().hex

def save_message(
    conversation_id: str,
    agent_name: str,
    message_type: str,
    content: str,
    metadata: Dict[str, Any] = None
):
    """
    Saves a single message or event to the database for a given conversation.

    Args:
        conversation_id: The ID of the current agent run.
        agent_name: The name of the agent or system component (e.g., 'Shyam', 'Tool').
        message_type: The type of message (e.g., 'plan', 'code', 'review', 'tool_output').
        content: The actual text content of the message.
        metadata: An optional dictionary for storing structured data (e.g., tool parameters).
    """
    conn = get_db_connection()
    try:
        # Convert metadata dict to a JSON string for storage.
        metadata_json = json.dumps(metadata) if metadata else None

        # Use parameterized queries to prevent SQL injection.
        conn.execute(
            """
            INSERT INTO conversations (conversation_id, agent_name, message_type, content, metadata)
            VALUES (?, ?, ?, ?, ?);
            """,
            (conversation_id, agent_name, message_type, content, metadata_json)
        )
    finally:
        conn.close()

def get_conversation_history(conversation_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves the full history of a conversation, ordered by timestamp.

    Args:
        conversation_id: The ID of the conversation to retrieve.

    Returns:
        A list of dictionaries, where each dictionary represents a message.
    """
    conn = get_db_connection()
    try:
        # Execute the query and fetch results as a list of dictionaries.
        # This is more convenient for the TUI to work with.
        result = conn.execute(
            """
            SELECT conversation_id, timestamp, agent_name, message_type, content, metadata
            FROM conversations
            WHERE conversation_id = ?
            ORDER BY timestamp ASC;
            """,
            (conversation_id,)
        ).fetch_df() # Fetching as a pandas DataFrame and converting to dict is easy.
        
        return result.to_dict('records')
    finally:
        conn.close()