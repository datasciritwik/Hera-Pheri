# src/hera_pheri/agents/tools.py

import subprocess
import shlex
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults
# from ..config import TAVILY_API_KEY
# ==============================================================================
# 🕵️‍♂️ SHARED TOOL: FOR SHYAM AND RAJU
# ==============================================================================

# This single instance can be added to both Shyam's and Raju's tool lists.
# It requires the TAVILY_API_KEY to be set in the .env file.

@tool
def web_search(query: str) -> str:
    """
    Performs a web search to find relevant URLs and returns a formatted string of the top results.
    The results are structured in <Document> tags with their source URL.
    Use this to research topics, find documentation, or get code examples.
    """
    print(f"--- Performing web search for: '{query}' ---")
    try:
        tavily_tool = TavilySearchResults(max_results=3) 
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

research_tools = [web_search]

# ==============================================================================
# 👳‍♂️ BABU BHAIYA'S TOOL: THE OPERATOR
# ==============================================================================

# ⚠️ SECURITY WARNING: This tool is extremely powerful and can execute any
# terminal command. Run any agent using this tool in a sandboxed environment
# like a Docker container to prevent unintended access to your system.

# Optional: allow only certain commands
SAFE_COMMANDS = ["ls", "echo", "pwd", "cat", "git", "mkdir", "python", "touch", "rm"]

@tool
def execute_terminal_command(command: str) -> str:
    """
    Executes a single shell command securely and returns the output or error.

    ⚠️ Use in sandboxed environments only.

    Accepts:
    - Git operations (e.g., git status)
    - File operations (e.g., ls -la, mkdir folder)
    - Python scripts (e.g., python script.py)

    Only one command should be passed at a time.
    """
    try:
        command = command.strip()

        if not command:
            return "Error: Command string is empty."

        # Optional: enforce command whitelist and check for natural language
        cmd_parts = shlex.split(command)
        if not cmd_parts or cmd_parts[0] not in SAFE_COMMANDS:
            return (
                f"Error: Command '{command}' is not a recognized or allowed shell command. "
                "If this is a plan step or description, please pass it to the coder agent to generate the actual command."
            )

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        # Truncate long output to prevent flooding
        MAX_OUTPUT_LENGTH = 3000
        if len(stdout) > MAX_OUTPUT_LENGTH:
            stdout = stdout[:MAX_OUTPUT_LENGTH] + "\n... [output truncated]"

        if result.returncode == 0:
            return f"✅ Command executed successfully.\n\n📤 Output:\n{stdout or '[No output]'}"
        else:
            return (
                f"❌ Command failed with return code {result.returncode}.\n\n"
                f"📤 Output:\n{stdout or '[No output]'}\n\n"
                f"⚠️ Error:\n{stderr or '[No stderr]'}"
            )

    except subprocess.TimeoutExpired:
        return "⏱️ Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"🚨 Unexpected error occurred: {str(e)}"