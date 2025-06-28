# src/hera_pheri/agents/graph.py

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import the state and node definitions from our local agent package
from src.agents.tools import execute_terminal_command
from src.agents.state import AgentState
from src.agents.definitions import (
    shyam_planner_node,
    raju_coder_node,
    shyam_reviewer_node,
    babu_bhaiya_llm_node,
    update_task_index_node
)

# ==============================================================================
# EDGES: The Routing Logic
# These functions determine the flow of the graph based on the current state.
# ==============================================================================

def should_code_or_execute(state: AgentState) -> str:
    """
    Router: Decides whether the current task requires coding or can be executed directly.
    """
    print("--- Router: Should Code or Execute? ---")
    current_task = state['plan'][state['current_task_index']]
    
    # A simple heuristic to decide if a task needs coding and review.
    # More complex logic could be added here.
    coding_keywords = ["write", "create a file", "python script", "code", "implement", "add content"]
    
    if any(keyword in current_task.lower() for keyword in coding_keywords):
        print(f"Decision: Task '{current_task}' requires coding. Routing to Raju.")
        return "code"
    else:
        # For simple commands like ls, mkdir, git init, etc.
        print(f"Decision: Task '{current_task}' is a direct command. Routing to Babu Bhaiya.")
        # We need to populate the 'code' field with the command for Babu Bhaiya
        state['code'] = current_task
        return "execute"

def after_review_router(state: AgentState) -> str:
    """
    Router: After Shyam's review, decides whether to execute or send back for revision.
    """
    print("--- Router: After Review ---")
    feedback = state.get('review_feedback', '').upper()
    
    if "APPROVED" in feedback:
        print("Decision: Code APPROVED. Routing to Babu Bhaiya for execution.")
        return "execute"
    else:
        print("Decision: Code REJECTED. Routing back to Raju for revision.")
        return "code" # This creates the review loop
    
def should_continue_or_end(state: AgentState) -> str:
    """
    Router: After a task index is updated, decides if the workflow should continue or end.
    """
    print("--- Router: Continue or End? ---")
    if state['current_task_index'] >= len(state['plan']):
        print("Decision: All tasks complete. Ending workflow.")
        return END
    else:
        print("Decision: More tasks remain. Looping back to plan check.")
        return "plan_check"

# ==============================================================================
# GRAPH ASSEMBLY
# ==============================================================================

def create_graph():
    """
    Assembles and compiles the LangGraph agent workflow.
    """
    workflow = StateGraph(AgentState)

    # --- Add Nodes ---
    workflow.add_node("plan", shyam_planner_node)
    workflow.add_node("code", raju_coder_node)
    workflow.add_node("review", shyam_reviewer_node)
    workflow.add_node("execute_llm", babu_bhaiya_llm_node)
    workflow.add_node("execute_tool", ToolNode([execute_terminal_command]))
    workflow.add_node("update_task_index", update_task_index_node) # <-- ADD THE NEW NODE
    workflow.add_node("plan_check", lambda state: state)

    # --- Set Entry Point ---
    workflow.set_entry_point("plan")

    # --- Add Edges ---
    workflow.add_edge("plan", "plan_check")
    workflow.add_edge("code", "review")
    workflow.add_edge("execute_llm", "execute_tool")
    
    # !!! NEW EDGE: After the tool runs, ALWAYS update the index !!!
    workflow.add_edge("execute_tool", "update_task_index")

    # --- Add Conditional Edges ---
    workflow.add_conditional_edges(
        "plan_check", should_code_or_execute, {"code": "code", "execute": "execute_llm"}
    )
    workflow.add_conditional_edges(
        "review", after_review_router, {"execute": "execute_llm", "code": "code"}
    )
    
    # !!! NEW ROUTING: After the index is updated, check if we should continue !!!
    workflow.add_conditional_edges(
        "update_task_index",
        should_continue_or_end,
        {
            "plan_check": "plan_check",
            END: END
        }
    )

    app = workflow.compile()
    print("Hera Pheri Crew graph compiled successfully with updated state logic!")
    return app

# Create a single, compiled instance of the graph
hera_pheri_crew = create_graph()