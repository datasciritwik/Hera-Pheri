from dataclasses import dataclass
from datetime import datetime

@dataclass
class Conversation:
    id: str
    session_id: str
    messages: list[str]
    created_at: datetime
    updated_at: datetime
    node_type: str
    llm_provider: str
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        
        if self.updated_at is None:
            self.updated_at = datetime.now()