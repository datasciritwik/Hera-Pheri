from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Conversation:
    session_id: str
    messages: list[str]
    node_type: str
    llm_provider: str
    id: str = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
            
        if self.created_at is None:
            self.created_at = datetime.now()
        
        if self.updated_at is None:
            self.updated_at = datetime.now()