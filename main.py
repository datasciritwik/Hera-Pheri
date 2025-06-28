from src.tui.app import HeraPheriApp
from src.database.connection import initialize_database
from src.config import init_config


def run_application():
    """
    Sets up and runs the main application.
    """
    # --- Step 0: Load environment variables and validate config ---
    init_config()

    # --- Step 1: Perform one-time setup ---
    initialize_database()

    # --- Step 2: Instantiate and run the TUI ---
    app = HeraPheriApp()
    app.run()
    print("\nThank you for using the Hera Pheri Crew! Goodbye!")


if __name__ == "__main__":
    # The `if __name__ == "__main__":` block is a standard Python practice.
    # It ensures that the `run_application()` function is called only when
    # this script is executed directly (e.g., `python main.py`), and not
    # when it's imported by another module.
    run_application()