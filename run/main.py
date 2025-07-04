import click
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from agents.graph import HeraPheriGraph
from database.storage import ConversationStorage
from llms.factory import LLMFactory
from config.settings import settings

console = Console()

class HeraPheriCLI:
    def __init__(self):
        self.console = Console()
        self.storage = ConversationStorage()
        self.current_session_id = None
        self.current_agent = None
        self.current_llm_provider = settings.DEFAULT_LLM_PROVIDER
        self.current_model = settings.DEFAULT_MODEL
        
    def display_welcome(self):
        """Display the welcome message and instructions."""
        welcome_text = """
        Welcome to HeraPheri CLI!
        -------------------------
        This is a command-line interface for interacting with HeraPheri agents.
        
        Commands:
        • Type your message to chat
        - `/sessions`: View conversation history
        - `/list-agents`: List all available agents
        - `/switch-llm`: Select an agent to interact with
        - `/new-session`: Start a new session with the selected agent
        - `/exit`: Exit the CLI
        - `/help`: Show this help message
        """
        self.console.print(Panel(welcome_text, title="Welcome to HeraPheri CLI", expand=False, border_style="blue"))
        
    def display_llm_providers(self):
        """Display available LLM providers"""
        providers = LLMFactory.get_available_providers()
        table = Table(title="Available LLM Providers")
        table.add_column("Provider", style="cyan")
        table.add_column("Status", style="green")
        
        for provider in providers:
            status = "✓ Available" if self._check_provider_config(provider) else "✗ Not configured"
            table.add_row(provider, status)
        
        self.console.print(table)
    
    def _check_provider_config(self, provider: str) -> bool:
        """Check if provider is properly configured"""
        config_map = {
            "openai": settings.OPENAI_API_KEY,
            "anthropic": settings.ANTHROPIC_API_KEY,
            "google": settings.GOOGLE_API_KEY,
            "groq": settings.GROQ_API_KEY
        }
        return bool(config_map.get(provider))
    
    def switch_llm_provider(self):
        """Allow user to switch LLM provider"""
        self.display_llm_providers()
        
        providers = LLMFactory.get_available_providers()
        available_providers = [p for p in providers if self._check_provider_config(p)]
        
        if not available_providers:
            self.console.print("❌ No LLM providers are configured. Please set up API keys.", style="red")
            return
        
        provider = Prompt.ask(
            "Choose LLM provider",
            choices=available_providers,
            default=self.current_llm_provider
        )
        
        if provider != self.current_llm_provider:
            self.current_llm_provider = provider
            # Restart agent with new provider
            if self.current_session_id:
                self.current_agent = HeraPheriGraph(
                    llm_provider=provider,
                    session_id=self.current_session_id
                )
            self.console.print(f"✓ Switched to {provider}", style="green")
    
    def start_new_session(self):
        """Start a new conversation session"""
        self.current_session_id = str(uuid.uuid4())
        self.current_agent = HeraPheriGraph(
            llm_provider=self.current_llm_provider,
            session_id=self.current_session_id
        )
        self.console.print(f"✓ Started new session: {self.current_session_id[:8]}...", style="green")
    
    def view_sessions(self):
        """View conversation history"""
        sessions = self.storage.get_all_sessions()
        
        if not sessions:
            self.console.print("No conversation history found.", style="yellow")
            return
        
        table = Table(title="Conversation Sessions")
        table.add_column("Session ID", style="cyan")
        table.add_column("Messages", style="magenta")
        table.add_column("Last Activity", style="green")
        
        for session_id in sessions[:10]:  # Show last 10 sessions
            history = self.storage.get_session_history(session_id)
            if history:
                last_activity = history[-1].timestamp.strftime("%Y-%m-%d %H:%M")
                table.add_row(
                    session_id[:8] + "...",
                    str(len(history)),
                    last_activity
                )
        
        self.console.print(table)
        
        # Ask if user wants to load a session
        if Confirm.ask("Load a previous session?"):
            session_input = Prompt.ask("Enter session ID (first 8 characters)")
            matching_sessions = [s for s in sessions if s.startswith(session_input)]
            
            if matching_sessions:
                self.current_session_id = matching_sessions[0]
                self.current_agent = HeraPheriGraph(
                    llm_provider=self.current_llm_provider,
                    session_id=self.current_session_id
                )
                self.console.print(f"✓ Loaded session: {self.current_session_id[:8]}...", style="green")
                
                # Show recent history
                history = self.storage.get_session_history(self.current_session_id)
                for conv in history[-3:]:  # Show last 3 messages
                    self.console.print(f"[blue]You:[/blue] {conv.user_message}")
                    self.console.print(f"[green]Agent:[/green] {conv.agent_response}")
                    self.console.print()
            else:
                self.console.print("❌ Session not found.", style="red")
                
                
    def agent_list(self):
        """List all available agents"""
        agent_list = """
        Available Agents:
        - `Shyam Planner and Reviewer`: A planning agent that helps you create and manage tasks.
        - `Raju Coder`: A coding agent that writes and reviews code.
        - `Babu Bhaiya Executor`: An executor agent that runs terminal commands and manages file operations.
        """
        
        self.console.print(Panel(agent_list, title="Available Agents", expand=False, border_style="blue"))
        
    def process_message(self, user_input:str):
        """Process user message through the agent"""
        if not self.current_agent:
            self.start_new_session()
            
        with self.console.status("[bold green]Processing..."):
            try:
                result = self.current_agent.process_message(user_input)
                
                response_style = "green" if result.success else "red"
                node_type = result.node_type if result.node_type else "Unknown"
                self.console.print(f"\n[{response_style}] Agent ({node_type}):[/{response_style}]")
                self.console.print(Panel(result["response"], border_style=response_style))
            except Exception as e:
                self.console.print(f"❌ Error: {str(e)}", style="red")
                
    def run(self):
        """Main loop to run the CLI"""
        self.display_welcome()
        
        # Check if any LLM provider is configured
        if not any(self._check_provider_config(p) for p in LLMFactory.get_available_providers()):
            self.console.print("❌ No LLM providers configured. Please set up API keys in .env file.", style="red")
            return
        self.display_llm_providers()
        self.switch_llm_provider()
        self.start_new_session()
        
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]").strip()
                
                if not user_input:
                    continue
                
                if user_input.startswith("/"):
                    if user_input == "/exit":
                        self.console.print("👋 Goodbye!", style="blue")
                        break
                    elif user_input == "/sessions":
                        self.view_sessions()
                    elif user_input == "/list-agents":
                        self.agent_list()
                    elif user_input == "/switch-llm":
                        self.switch_llm_provider()
                    elif user_input == "/help":
                        self.display_welcome()
                    elif user_input == "/new-session":
                        if Confirm.ask("Are you sure you want to start a new session?"):
                            self.start_new_session()
                        else:
                            self.console.print("❌ New session cancelled.", style="red")
                    else:
                        self.console.print("❌ Unknown command. Type '/help' for available commands.", style="red")
                else:
                    # Process regular message
                    self.process_message(user_input)
                                    
                
            except KeyboardInterrupt:
                self.console.print("\n👋 Goodbye!", style="blue")
                break
            except Exception as e:
                self.console.print(f"❌ Unexpected error: {str(e)}", style="red")
                
@click.command()
@click.version_option(version="1.0.0", message="HeraPheri CLI v%(version)s")
@click.option("--provider", default=settings.DEFAULT_LLM_PROVIDER, help="LLM provider to use")
@click.option("--model", default=settings.DEFAULT_MODEL, help="LLM model to use")
@click.option("--session", default=None, help="Session ID to load")
def main(provider, model, session):
    """Run the HeraPheri CLI."""
    cli = HeraPheriCLI()
    
    # Set initial provider and model
    cli.current_llm_provider = provider
    cli.current_model = model
    
    if session:
        cli.current_session_id = session
        cli.current_agent = HeraPheriGraph(
            llm_provider=provider,
            session_id=session
        )
    
    cli.run()
    
if __name__ == "__main__":
    main()