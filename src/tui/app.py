from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input
from textual import work  # <-- THIS IS THE CORRECTED IMPORT

from ..agents.graph import hera_pheri_crew
from ..agents.state import AgentState
from ..database import operations as db_ops
from .widgets import LogWidget

# Define agent-specific colors for the UI
AGENT_STYLES = {
    "Shyam": "bold cyan",
    "Raju": "bold magenta",
    "Babu Bhaiya": "bold yellow",
    "System": "bold green",
    "Error": "bold red",
}

class HeraPheriApp(App):
    """The main Textual application for the Hera Pheri agent crew."""
    
    CSS_PATH = "app.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="app-grid"):
            yield LogWidget(id="log_view")
            yield Input(placeholder="Enter your task for the crew...", id="task_input")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.query_one("#task_input").focus()
        self.log_message("System", "Welcome to Hera Pheri Crew! Enter a task to begin.", AGENT_STYLES["System"])

    def log_message(self, agent: str, message: str, style: str = "white"):
        """Thread-safe method to add a message to the log."""
        log_widget = self.query_one(LogWidget)
        log_widget.add_log_message(agent, message, style)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Called when the user presses Enter in the input box."""
        task = event.value
        if not task:
            return
            
        input_widget = self.query_one("#task_input")
        input_widget.disabled = True
        input_widget.placeholder = "Agent is running... please wait."
        input_widget.clear()

        self.run_agent_task(task)

    @work(exclusive=True, thread=True)
    def run_agent_task(self, task: str) -> None:
        """
        Runs the agent graph in a background thread to avoid freezing the UI.
        """
        try:
            self.call_from_thread(self.log_message, "System", f"Starting new task: {task}", AGENT_STYLES["System"])
            
            conversation_id = db_ops.create_conversation_id()
            initial_state: AgentState = {
                "task": task,
                "plan": None,
                "code": None,
                "review_feedback": None,
                "current_task_index": 0,
                "messages": [],
            }

            for event in hera_pheri_crew.stream(initial_state, {"recursion_limit": 100}):
                node_name = list(event.keys())[0]
                node_state = event[node_name]

                if node_name == "plan":
                    self.call_from_thread(self.log_message, "Shyam", f"Created Plan:\n" + "\n".join(f"- {s}" for s in node_state['plan']), AGENT_STYLES["Shyam"])
                    db_ops.save_message(conversation_id, "Shyam", "plan", "\n".join(node_state['plan']))
                elif node_name == "code":
                    self.call_from_thread(self.log_message, "Raju", f"Wrote Code:\n---\n{node_state['code']}\n---", AGENT_STYLES["Raju"])
                    db_ops.save_message(conversation_id, "Raju", "code", node_state['code'])
                elif node_name == "review":
                    feedback = node_state['review_feedback']
                    style = "green" if "APPROVED" in feedback else "yellow"
                    self.call_from_thread(self.log_message, "Shyam", f"Review Feedback: {feedback}", f"bold {style}")
                    db_ops.save_message(conversation_id, "Shyam", "review", feedback)
                elif node_name == "execute_tool":
                    self.call_from_thread(self.log_message, "Babu Bhaiya", f"Executed Tool. Output received.", AGENT_STYLES["Babu Bhaiya"])
            
            self.call_from_thread(self.log_message, "System", "Task completed successfully!", AGENT_STYLES["System"])

        except Exception as e:
            self.call_from_thread(self.log_message, "Error", f"An error occurred: {e}", AGENT_STYLES["Error"])
        
        finally:
            def re_enable_input():
                input_widget = self.query_one("#task_input")
                input_widget.disabled = False
                input_widget.placeholder = "Enter your task for the crew..."
                input_widget.focus()
            
            self.call_from_thread(re_enable_input)