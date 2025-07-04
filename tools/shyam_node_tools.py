from agents.tool import web_search
from pydantic import BaseModel
from typing import Type

class ShyamNodeToolInput(BaseModel):
    """Input for the ShyamNodeTool."""
    content: str
    
class WebSearchTool(BaseModel):
    name: str = "web_search"
    description: str = "Performs a web search to find relevant URLs and returns a formatted string of the top results. Use this to research topics, find documentation, or get code examples."
    args_schema: Type[BaseModel] = ShyamNodeToolInput
    
    def _run(self, content: str) -> str:
        """
        Perform a web search with the given content.
        
        Args:
            content (str): The search query.
        
        Returns:
            str: Formatted search results.
        """
        return web_search(content)
    
    async def _arun(self, content: str) -> str:
        return self._run(content)