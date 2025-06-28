from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import re

# Import the state and tools from our local agent package
from src.agents.state import AgentState
from src.agents.tools import web_search, execute_terminal_command

# --- Agent LLM Configuration ---
# We can use a powerful model for planning and review, and a faster one for other tasks if desired.
# For simplicity, we'll use deepseek-r1-distill-llama-70b for all.
shyam_llm = ChatGroq(model="deepseek-r1-distill-llama-70b")
raju_llm = ChatGroq(model="deepseek-r1-distill-llama-70b")
babu_llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

# --- Agent Runner Helper ---
# This helper function creates a runnable agent instance from a system prompt and tools.
def create_agent_runner(llm: ChatGroq, system_prompt: str, tools: list):
    """Creates a LangChain agent runner."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    llm_with_tools = llm.bind_tools(tools)
    return prompt | llm_with_tools

def update_task_index_node(state: AgentState):
    """
    Increments the task index after a task has been successfully executed.
    This is a dedicated node to ensure state is updated reliably.
    """
    print("--- System: Updating task index. ---")
    new_index = state.get('current_task_index', 0) + 1
    return {"current_task_index": new_index}

# ==============================================================================
# 🤵 SHYAM: THE PLANNER & REVIEWER
# ==============================================================================

def shyam_planner_node(state: AgentState):
    """
    Takes the initial task and creates a detailed, step-by-step plan.
    """
    print("--- 🤵 Shyam: Meticulously planning the task... ---")
    
    system_prompt = """You are Shyam, the meticulous planner of the group. Your job is to take a user's request and create a clear, step-by-step plan.
- The plan must be a sequence of **valid, executable shell commands** or tasks for Raju to code.
- Each step must be a single, concrete action.
- For file system operations, use commands like `mkdir`, `touch`, `ls`, etc.
- To write content to a file, use a step like: `Write the following Python code to main.py:` followed by the code block.
- **Example of a good plan:**
    1. mkdir my_project
    2. cd my_project
    3. Write the following Python code to main.py:
    4. pip install fastapi uvicorn
    5. uvicorn main:app --reload

- **Respond ONLY with the numbered list of steps.** Do not add any other text, headers, or explanations."""
    
    planner_runner = create_agent_runner(shyam_llm, system_prompt, [web_search])
    response = planner_runner.invoke({"input": state['task']})
    
    plan = []
    try:
        plan_steps = response.content.strip().split('\n')
        for step in plan_steps:
            if '.' in step:
                # Get content after the first period
                plan.append(step.split('.', 1)[1].strip())
    except Exception as e:
        print(f"Error parsing plan: {e}")
        # Handle error, maybe return an empty plan or an error state
        return {"plan": [], "current_task_index": 0}


    return {"plan": plan, "current_task_index": 0}

def shyam_reviewer_node(state: AgentState):
    """
    Reviews the code written by Raju and provides feedback.
    """
    print("--- 🤵 Shyam: Reviewing Raju's code with high standards... ---")

    system_prompt = """You are Shyam, and you are reviewing the code written by Raju.
- Your standards are very high. Check for correctness, bugs, efficiency, and adherence to the task.
- The current task and the code to review are provided.
- If the code is perfect and meets the requirements of the task, respond with ONLY the word "APPROVED".
- If there are any issues, provide concise, critical, and actionable feedback for Raju to fix it. Do NOT approve it. Explain what is wrong and why."""
    
    reviewer_runner = create_agent_runner(shyam_llm, system_prompt, [web_search])
    current_task = state['plan'][state['current_task_index']]
    review_input = f"Current Task: {current_task}\n\nCode to Review:\n```\n{state['code']}\n```"
    response = reviewer_runner.invoke({"input": review_input})

    return {"review_feedback": response.content}

# ==============================================================================
# 👨‍💻 RAJU: THE CODER
# ==============================================================================

def raju_coder_node(state: AgentState):
    """
    Writes code for a given task, potentially with feedback from Shyam.
    """
    print("--- 👨‍💻 Raju: Writing code... Fast and clever! ---")

    system_prompt = """You are Raju, the fast-moving coder. Your job is to take a SINGLE task and write the code or command for it.
- Focus only on the current task. Do not try to do more.
- Write the full code or terminal command required.
- If the task is to write a python script, respond with ONLY the complete python code, inside a ```python ... ``` block. Nothing else.
- If the task is a terminal command, respond with ONLY the command itself.
- You might receive critical feedback from Shyam. If so, you MUST apply the feedback to fix your previous work."""

    coder_runner = create_agent_runner(raju_llm, system_prompt, [web_search])
    current_task = state['plan'][state['current_task_index']]
    
    # Build the input for Raju, including feedback if it exists
    request = f"Your task is: {current_task}"
    if state.get('review_feedback') and "APPROVED" not in state['review_feedback']:
        request += f"\n\nThis is your second attempt. Shyam provided this feedback, you MUST fix it:\n{state['review_feedback']}"

    response = coder_runner.invoke({"input": request})
    
    # Clean up the code from markdown code blocks if they exist
    code = response.content.strip()
    # Remove triple backtick code block with or without language
    code = re.sub(r"^```[a-zA-Z0-9]*\n", "", code)
    code = re.sub(r"\n?```$", "", code)

    # Clear old feedback and add the new code
    return {"code": code.strip(), "review_feedback": ""}

# ==============================================================================
# 👳‍♂️ BABU BHAIYA: THE OPERATOR
# ==============================================================================

def babu_bhaiya_llm_node(state: AgentState):
    """
    Asks Babu Bhaiya's LLM to choose the correct tool call for the given command.
    """
    print("--- 👳‍♂️ Babu Bhaiya: Okay, what's the command... ---")

    system_prompt = """You are Babu Bhaiya. You only execute commands and don't ask questions.
You will be given a command to run. You MUST use the `execute_terminal_command` tool to run it.
Do not add any commentary. Just call the tool with the provided command."""
    
    # Create the runner for Babu Bhaiya, binding his specific tool
    executor_runner = create_agent_runner(babu_llm, system_prompt, [execute_terminal_command])
    
    command_to_execute = (state.get('code') or '').strip()
    if not command_to_execute:
        command_to_execute = state['plan'][state['current_task_index']]
        
    print(f"Preparing to execute: '{command_to_execute}'")
    
    # This will produce an AIMessage with a `tool_calls` attribute
    response = executor_runner.invoke({"input": command_to_execute})
    
    # We return the entire response object so the graph can access tool_calls
    return {"messages": [response]}