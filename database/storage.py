import duckdb
from typing import List, Optional
from database.models import Conversation
from config.settings import settings
from json import dumps, loads

class ConversationStorage:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.DB_PATH
        # We'll keep one persistent connection
        self.conn = duckdb.connect(self.db_path)
        self.init_database()

    def init_database(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            messages VARCHAR NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            node_type TEXT,
            llm_provider TEXT
        );
        """)

    def create(self, convo: Conversation):
        """Insert a new conversation record."""
        self.conn.execute("""
        INSERT INTO conversations
        (id, session_id, messages, created_at, updated_at, node_type, llm_provider)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            convo.id,
            convo.session_id,
            dumps(convo.messages),
            convo.created_at,
            convo.updated_at,
            convo.node_type,
            convo.llm_provider
        ))

    def update(self, convo: Conversation):
        """Overwrite an existing conversation (by id)."""
        convo.updated_at = convo.updated_at
        self.conn.execute("""
        UPDATE conversations SET
            session_id = ?,
            messages   = ?,
            updated_at = ?,
            node_type  = ?,
            llm_provider = ?
        WHERE id = ?
        """, (
            convo.session_id,
            dumps(convo.messages),
            convo.updated_at,
            convo.node_type,
            convo.llm_provider,
            convo.id
        ))

    def get_by_id(self, convo_id: str) -> Optional[Conversation]:
        """Fetch a Conversation by its ID."""
        res = self.conn.execute("""
            SELECT id, session_id, messages, created_at, updated_at, node_type, llm_provider
            FROM conversations
            WHERE id = ?
        """, (convo_id,)).fetchone()
        if not res:
            return None
        msgs = loads(res[2])
        return Conversation(
            id=res[0],
            session_id=res[1],
            messages=msgs,
            created_at=res[3],
            updated_at=res[4],
            node_type=res[5],
            llm_provider=res[6]
        )

    def get_by_session(self, session_id: str) -> List[Conversation]:
        """Fetch all conversations in a session."""
        rows = self.conn.execute("""
            SELECT id, session_id, messages, created_at, updated_at, node_type, llm_provider
            FROM conversations
            WHERE session_id = ?
            ORDER BY created_at
        """, (session_id,)).fetchall()
        convos = []
        for res in rows:
            convos.append(Conversation(
                id=res[0],
                session_id=res[1],
                messages=loads(res[2]),
                created_at=res[3],
                updated_at=res[4],
                node_type=res[5],
                llm_provider=res[6]
            ))
        return convos

    def append_message(self, convo_id: str, message: str):
        """Add a single message to the conversation’s message list."""
        convo = self.get_by_id(convo_id)
        if not convo:
            raise KeyError(f"No conversation with id {convo_id}")
        convo.messages.append(message)
        self.update(convo)
        
    def close(self):
        """Close the DuckDB connection when done."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()
        