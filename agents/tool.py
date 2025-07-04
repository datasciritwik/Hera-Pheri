from langchain_community.tools import TavilySearchResults
from typing import Optional
import platform
import os
import subprocess
import shutil
import json
import sys

# ***************** File handling tools *****************

def create_file(file_path: str, content: str) -> str:
    """Create a file with the specified content."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{file_path}' created successfully."
    except Exception as e:
        return f"Error creating file '{file_path}': {str(e)}"
    
def update_file(file_path: str, content: str) -> str:
    """Update a file with the specified content."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"File '{file_path}' updated successfully."
    except Exception as e:
        return f"Error updating file '{file_path}': {str(e)}"

# ***************** Web Search Tool *****************

def web_search(query: str) -> str:
    """
    Performs a web search to find relevant URLs and returns a formatted string of the top results.
    The results are structured in <Document> tags with their source URL.
    Use this to research topics, find documentation, or get code examples.
    """
    print(f"--- Performing web search for: '{query}' ---")
    try:
        tavily_tool = TavilySearchResults(max_results=5) 
        search_results = tavily_tool.invoke({"query": query})

        if not search_results:
            return "No search results found for that query."

        # Format the results into the structured XML-like format for clarity
        formatted_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
                for doc in search_results
            ]
        )
        return formatted_docs
    
    except Exception as e:
        return f"An error occurred during web search: {e}"
    
# ***************** Terminal Command Tool *****************

def execute_terminal_command(
    command: str, 
    working_directory: Optional[str] = None,
    timeout: Optional[int] = 30,
    capture_output: bool = True,
    shell: bool = True
) -> str:
    """Execute any terminal/command line command and return the output.
    
    This tool can handle all types of terminal commands including:
    - File operations (ls, cp, mv, rm, mkdir, etc.)
    - Git commands (git clone, git commit, git push, etc.)
    - Package management (pip, npm, apt, brew, etc.)
    - System commands (ps, top, df, etc.)
    - Development tools (python, node, docker, etc.)
    - Text processing (grep, sed, awk, etc.)
    
    Args:
        command: The terminal command to execute (e.g., "ls -la", "git status")
        working_directory: Optional directory to run the command in
        timeout: Maximum time to wait for command completion in seconds (default: 30)
        capture_output: Whether to capture and return output (default: True)
        shell: Whether to run command through shell (default: True)
    
    Returns:
        String containing the command output, error messages, and execution status
    """
    
    try:
        # Store original directory
        original_dir = os.getcwd()
        
        # Change to working directory if specified
        if working_directory:
            if os.path.exists(working_directory):
                os.chdir(working_directory)
            else:
                return f"Error: Working directory '{working_directory}' does not exist"
        
        # Prepare command execution
        if platform.system() == "Windows":
            # Windows-specific handling
            if not shell:
                command = command.split()
        
        # Execute the command
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            cwd=working_directory
        )
        
        # Prepare output
        output_parts = []
        
        # Add command info
        output_parts.append(f"Command: {command}")
        if working_directory:
            output_parts.append(f"Working Directory: {working_directory}")
        
        # Add stdout if available
        if result.stdout:
            output_parts.append("--- STDOUT ---")
            output_parts.append(result.stdout.strip())
        
        # Add stderr if available
        if result.stderr:
            output_parts.append("--- STDERR ---")
            output_parts.append(result.stderr.strip())
        
        # Add return code
        output_parts.append(f"--- RETURN CODE ---")
        output_parts.append(f"Exit Code: {result.returncode}")
        
        # Determine if command was successful
        if result.returncode == 0:
            output_parts.append("Status: SUCCESS")
        else:
            output_parts.append("Status: FAILED")
        
        return "\n".join(output_parts)
        
    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after {timeout} seconds"
    
    except subprocess.CalledProcessError as e:
        return f"Error: Command '{command}' failed with exit code {e.returncode}\nOutput: {e.output}\nError: {e.stderr}"
    
    except FileNotFoundError:
        return f"Error: Command '{command}' not found. Make sure the command/program is installed and in PATH"
    
    except PermissionError:
        return f"Error: Permission denied when executing '{command}'"
    
    except Exception as e:
        return f"Unexpected error executing '{command}': {str(e)}"
    
    finally:
        # Always restore original directory
        try:
            os.chdir(original_dir)
        except:
            pass
  
def get_system_info() -> str:
    """Get comprehensive system information including OS, Python version, and available tools."""
    
    info = {
        "Operating System": platform.system(),
        "OS Release": platform.release(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),
        "Python Version": sys.version,
        "Current Working Directory": os.getcwd(),
        "Environment Variables": dict(os.environ),
        "Available Commands": {}
    }
    
    # Check for common development tools
    common_tools = [
        "git", "python", "python3", "pip", "pip3", "node", "npm", "docker", 
        "kubectl", "java", "javac", "gcc", "make", "cmake", "curl", "wget"
    ]
    
    for tool in common_tools:
        if shutil.which(tool):
            info["Available Commands"][tool] = shutil.which(tool)
    
    return json.dumps(info, indent=2, default=str)

def change_directory(path: str) -> str:
    """Change the current working directory.
    
    Args:
        path: The directory path to change to
    """
    try:
        if os.path.exists(path) and os.path.isdir(path):
            os.chdir(path)
            return f"Successfully changed directory to: {os.getcwd()}"
        else:
            return f"Error: Directory '{path}' does not exist or is not a directory"
    except Exception as e:
        return f"Error changing directory: {str(e)}"

def list_directory(path: Optional[str] = None, show_hidden: bool = False) -> str:
    """List contents of a directory with detailed information.
    
    Args:
        path: Directory path to list (default: current directory)
        show_hidden: Whether to show hidden files (default: False)
    """
    try:
        target_path = path or os.getcwd()
        
        if not os.path.exists(target_path):
            return f"Error: Path '{target_path}' does not exist"
        
        if not os.path.isdir(target_path):
            return f"Error: Path '{target_path}' is not a directory"
        
        items = []
        for item in os.listdir(target_path):
            if not show_hidden and item.startswith('.'):
                continue
                
            item_path = os.path.join(target_path, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path) if not is_dir else 0
            
            items.append({
                "name": item,
                "type": "directory" if is_dir else "file",
                "size": size
            })
        
        # Sort items: directories first, then files
        items.sort(key=lambda x: (x["type"] == "file", x["name"].lower()))
        
        result = [f"Contents of: {target_path}"]
        result.append("-" * 50)
        
        for item in items:
            type_indicator = "📁" if item["type"] == "directory" else "📄"
            size_info = f"({item['size']} bytes)" if item["type"] == "file" else ""
            result.append(f"{type_indicator} {item['name']} {size_info}")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"Error listing directory: {str(e)}"


# ***************** Task Node Tools *****************
def load_markdown(path: str = "plan_output.md") -> str:
    """Loads the markdown file from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_markdown(markdown: str, path: str = "plan_output.md") -> str:
    """Saves markdown content to file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(markdown)
    return "Markdown saved."

