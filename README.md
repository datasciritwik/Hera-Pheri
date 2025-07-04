# Hera Pheri: An Autonomous AI Coding Crew 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-f06925)](https://github.com/langchain-ai/langgraph)


<h3 align="center">
  <code>pip install herapheri</code>
</h3>


An experimental autonomous AI agent system built with LangGraph that plans, writes, reviews, and executes code to complete complex tasks. The system is inspired by the iconic characters from the movie *Hera Pheri*, with each agent embodying a unique persona and role.

-   **Shyam:** The meticulous planner and reviewer.
-   **Raju:** The fast-moving, clever coder.
-   **Babu Bhaiya:** The reliable operator who interacts with the terminal.

## Core Concept

The project demonstrates a multi-agent collaboration pattern where complex tasks are broken down and handled by specialized AI agents. This "separation of concerns" creates a robust and fault-tolerant system:

1.  **Planning:** Shyam receives a high-level goal and creates a detailed, step-by-step execution plan.
2.  **Coding & Review Loop:** Raju takes one task at a time and writes the necessary code, which is then passed to Shyam for rigorous review. If the code fails review, it's sent back to Raju with feedback. This loop ensures code quality.
3.  **Execution:** Once a piece of code is approved by Shyam, it's handed to Babu Bhaiya, who is the only agent with permission to execute terminal commands (like writing to files, running git, etc.).

## Workflow Diagram

This diagram illustrates the core logic and flow of control between the agents.

```mermaid
graph TD
    Start([User Request]) --> Plan[Shyam: Creates Plan using Web Search --Tool]
    
    Plan --> CheckTasks{Tasks Remaining?}
    
    CheckTasks -- Yes --> Code[Raju: Writes Code for Task using Web Search --Tool]
    
    Code --> Review[Shyam: Reviews Code]
    
    Review --> QualityCheck{Code Approved?}
    
    QualityCheck -- No --> Code
    
    QualityCheck -- Yes --> Execute[Babu Bhaiya: Runs Commands using Terminal --Tool]
    
    Execute --> CheckTasks
    
    CheckTasks -- No --> End([Project Complete])
```

## Folder Structure

```
├── README.md
├── agents
│   ├── __init__.py
│   ├── graph.py
│   ├── nodes.py
│   ├── state.py
│   └── tool.py
├── config
│   ├── __init__.py
│   └── settings.py
├── database
│   ├── __init__.py
│   ├── models.py
│   └── storage.py
├── llms
│   ├── __init__.py
│   ├── factory.py
│   └── providers.py
├── notebooks
│   └── test.ipynb
├── requirements-test.txt
├── requirements.txt
├── run
│   └── main.py
├── setup.py
└── tools
    ├── __init__.py
    ├── babu_bhaiya_node_tools.py
    ├── raju_node_tools.py
    ├── shyam_node_tools.py
    └── task_node_tools.py
```

**Framework:** LangGraph

**Clone the repository:**
```sh
git clone https://github.com/datasciritwik/Hera-Pheri.git
cd Hera-Pheri
```

``` sh
pip install -e .
```

## Using API

```sh
herapheri --provider <LLM PROVIDER NAME> --model <MODEL NAME>
```
## ⚠️ Security Warning

This project uses an AI agent (`Babu Bhaiya`) that can **execute arbitrary terminal commands**. This is extremely powerful and potentially dangerous. It can modify your file system, access sensitive information, and interact with the internet.

**It is strongly recommended to run this project in a sandboxed, isolated environment, such as a Docker container, to prevent unintended consequences.**

## Contributing

Contributions are welcome! If you have ideas for new features, tools, or improvements to the agent logic, feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
