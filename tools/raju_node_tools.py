from agents.tool import create_file, update_file
from pydantic import BaseModel
from langchain.tools import BaseTool
from typing import Type, Optional

class RajuNodeToolInput(BaseModel):
    """Input for the RajuNodeTool."""
    content: Optional[str] = None
    filepath: str
    
class CreateFileTool(BaseTool):
    name: str = "create_file"
    description: str = "Creates a file with the specified content."
    args_schema: Type[BaseModel] = RajuNodeToolInput
    
    def _run(self, filepath: str, content: str) -> str:
        """
        Create a file with the specified content.
        
        Args:
            filepath (str): The path to the file to create.
            content (str): The content to write to the file.
        
        Returns:
            str: Confirmation message.
        """
        return create_file(filepath, content)
    
    async def _arun(self, filepath: str, content: str) -> str:
        return self._run(filepath, content)
    
class UpdateFileTool(BaseTool):
    name: str = "update_file"
    description: str = "Updates a file with the specified content."
    args_schema: Type[BaseModel] = RajuNodeToolInput
    
    def _run(self, filepath: str, content: str) -> str:
        """
        Update a file with the specified content.
        
        Args:
            filepath (str): The path to the file to update.
            content (str): The content to append to the file.
        
        Returns:
            str: Confirmation message.
        """
        return update_file(filepath, content)
    
    async def _arun(self, filepath: str, content: str) -> str:
        return self._run(filepath, content)