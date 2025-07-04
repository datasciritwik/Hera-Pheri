from agents.tool import execute_terminal_command, change_directory, get_system_info, list_directory
from pydantic import BaseModel
from typing import Type, Optional

class BabuBhaiyaNodeToolInput(BaseModel):
    """Input for the BabuBhaiyaNodeTool."""
    command: str
    working_directory: Optional[str] = None
    timeout: Optional[int] = 30
    capture_output: Optional[bool] = True
    shell: Optional[bool] = True
    
class TerminalCmdNodeTool(BaseModel):
    name: str = "terminal_command"
    description: str = "Executes a terminal command and returns the output."
    args_schema: Type[BaseModel] = BabuBhaiyaNodeToolInput
    
    def _run(self, command: str, working_directory: Optional[str] = None, 
             timeout: Optional[int] = 30, capture_output: Optional[bool] = True, 
             shell: Optional[bool] = True) -> str:
        """
        Execute a terminal command and return the output.
        
        Args:
            command (str): The terminal command to execute.
            working_directory (Optional[str]): Directory to run the command in.
            timeout (Optional[int]): Maximum time to wait for command completion.
            capture_output (Optional[bool]): Whether to capture and return output.
            shell (Optional[bool]): Whether to run command through shell.
        
        Returns:
            str: Command output or error message.
        """
        return execute_terminal_command(command, working_directory, timeout, capture_output, shell)
    
    async def _arun(self, command: str, working_directory: Optional[str] = None, 
                    timeout: Optional[int] = 30, capture_output: Optional[bool] = True, 
                    shell: Optional[bool] = True) -> str:
        return self._run(command, working_directory, timeout, capture_output, shell)
    
    
class ChangeDirectoryNodeTool(BaseModel):
    name: str = "change_directory"
    description: str = "Changes the current working directory."
    args_schema: Type[BaseModel] = BabuBhaiyaNodeToolInput
    
    def _run(self, working_directory: str) -> str:
        """
        Change the current working directory.
        
        Args:
            working_directory (str): The directory to change to.
        
        Returns:
            str: Confirmation message or error.
        """
        return change_directory(working_directory)
    
    async def _arun(self, working_directory: str) -> str:
        return self._run(working_directory)
    
class SystemInfoNodeTool(BaseModel):
    name: str = "system_info"
    description: str = "Retrieves system information."
    args_schema: Type[BaseModel] = BabuBhaiyaNodeToolInput
    
    def _run(self) -> str:
        """
        Retrieve system information.
        
        Returns:
            str: System information.
        """
        return get_system_info()
    
    async def _arun(self) -> str:
        return self._run()