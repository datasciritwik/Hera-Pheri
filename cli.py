# cli.py

# A simple Command-Line Interface (CLI) for testing the Hera Pheri agent crew directly.
# This bypasses the Textual UI for quick, raw interaction with the agent graph.

import sys
from rich.console import Console
from rich.panel import Panel

# Ensure the 'src' directory is in the Python path
# This is necessary to import from the 'hera_pheri' package
sys.path.append('src')

from src.agents.graph import hera_pheri_crew
from src.agents.state import AgentState
from src.database.connection import initialize_database

# Initialize Rich console for better printing
console = Console()

def main():
    """
    Main function to run the command-line interface.
    """
    # --- Step 1: Perform one-time setup ---
    initialize_database()

    console.print(Panel("[bold cyan]Hera Pheri Crew: Simple CLI Tester[/bold cyan]", 
                      title="Welcome!", subtitle="[dim](Type 'quit' or 'exit' to stop)[/dim]"))

    # --- Step 2: Start the interactive loop ---
    while True:
        try:
            task = console.input("[bold green]Task for the crew > [/bold green]")

            if task.lower() in ["quit", "exit"]:
                console.print("\n[bold yellow]Goodbye![/bold yellow]")
                break
            
            if not task.strip():
                continue

            # --- Step 3: Run the agent ---
            console.print("\n[bold blue]--- Starting Agent Run ---[/bold blue]")
            
            initial_state: AgentState = {
                "task": task,
                "plan": None,
                "code": None,
                "review_feedback": None,
                "current_task_index": 0,
                "messages": [],
            }

            # Stream the events from the graph to see the flow in real-time
            for event in hera_pheri_crew.stream(initial_state, {"recursion_limit": 100}):
                node_name = list(event.keys())[0]
                node_state = event[node_name]

                console.rule(f"[bold yellow] Node: {node_name} [/bold yellow]")

                if node_name == "plan":
                    console.print("[bold cyan]🤵 Shyam's Plan:[/bold cyan]")
                    for i, step in enumerate(node_state['plan'], 1):
                        console.print(f"  {i}. {step}")
                elif node_name == "code":
                    console.print("[bold magenta]👨‍💻 Raju's Code:[/bold magenta]")
                    console.print(f"```python\n{node_state['code']}\n```")
                elif node_name == "review":
                    feedback = node_state['review_feedback']
                    if "APPROVED" in feedback:
                        console.print(f"[bold green]🤵 Shyam's Review: {feedback}[/bold green]")
                    else:
                        console.print(f"[bold yellow]🤵 Shyam's Review: {feedback}[/bold yellow]")
                elif node_name == "execute_tool":
                    tool_output = node_state['messages'][-1].content
                    console.print(f"[bold yellow]👳‍♂️ Babu Bhaiya's Tool Output:[/bold yellow]\n{tool_output}")
                
                console.print() # Add a newline for spacing

            console.print(Panel("[bold green]✅ Task Completed Successfully![/bold green]"))

        except KeyboardInterrupt:
            console.print("\n[bold red]Interrupted by user. Exiting.[/bold red]")
            break
        except Exception as e:
            console.print(Panel(f"[bold red]An error occurred during the agent run:[/bold red]\n{e}", 
                                title="[bold red]Error[/bold red]", border_style="red"))
            continue

if __name__ == "__main__":
    main()