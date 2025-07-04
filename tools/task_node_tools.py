from agents.tool import load_markdown, save_markdown
from pydantic import BaseModel
from langchain.tools import BaseTool
from typing import Optional, Type

class TaskNodeToolInput(BaseModel):
    """Input for the TaskNodeTool."""
    query: Optional[str]
    filepath: str

class LoadMarkdownTool(BaseTool):
    name: str = "load_markdown"
    description: str = "Loads a markdown file and returns its content."
    args_schema: Type[BaseModel] = TaskNodeToolInput
    
    def _run(self, filepath: str = "task.md") -> str:
        """
        Load a markdown file and return its content.
        
        Args:
            filepath (str): The path to the markdown file to load.
        
        Returns:
            str: The content of the markdown file.
        """
        try:
            # Attempt to load the markdown file
            content = load_markdown(filepath)
            if not content:
                raise FileNotFoundError(f"Markdown file '{filepath}' not found or is empty.")
        except FileNotFoundError as e:
            return f"Error: {e}"
        return content
    
    async def _arun(self, query: Optional[str] = None, filepath: str = "task.md") -> str:
        return self._run(query, filepath)
    
class SaveMarkdownTool(BaseTool):
    name: str = "save_markdown"
    description: str = "Saves content to a markdown file."
    args_schema: Type[BaseModel] = TaskNodeToolInput
    
    def _run(self, query: Optional[str] = None, filepath: str = "task.md") -> str:
        """
        Save content to a markdown file.
        
        Args:
            query (Optional[str]): The content to save.
            filepath (str): The path to the markdown file to save.
        
        Returns:
            str: Confirmation message.
        """
        try:
            # Attempt to save the content to the markdown file
            save_markdown(query, filepath)
        except Exception as e:
            return f"Error saving markdown file: {e}"
        return f"Markdown file '{filepath}' saved successfully."
    
    async def _arun(self, query: Optional[str] = None, filepath: str = "task.md") -> str:
        return self._run(query, filepath)