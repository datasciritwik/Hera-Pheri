import duckdb
import os

# Define the path for the database file within the project structure.
DB_FILE = "data/conversations.duckdb"

def get_db_connection():
    """
    Establishes and returns a connection to the DuckDB database.
    Creates the database file and directories if they don't exist.
    """
    # Ensure the 'data' directory exists.
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    # Connect to the database file.
    return duckdb.connect(database=DB_FILE, read_only=False)

def initialize_database():
    """
    Initializes the database by creating the main 'conversations' table
    if it does not already exist. This function is safe to call on every
    application startup.
    """
    print("--- Initializing Database ---")
    conn = get_db_connection()
    try:
        # Use 'CREATE TABLE IF NOT EXISTS' to be idempotent.
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                conversation_id VARCHAR NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT now(),
                agent_name VARCHAR NOT NULL,
                message_type VARCHAR NOT NULL, -- e.g., 'thought', 'tool_call', 'tool_output'
                content TEXT NOT NULL,
                metadata JSON
            );
        """)
        print("Database table 'conversations' is ready.")
    finally:
        # Always close the connection after setup.
        conn.close()