from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any
from llms.factory import LLMFactory
from agents.state import HeraPheriState, Prompts
from tools.shyam_node_tools import WebSearchTool

from tools.task_node_tools import LoadMarkdownTool, SaveMarkdownTool
from tools.raju_node_tools import CreateFileTool, UpdateFileTool
from tools.babu_bhaiya_node_tools import TerminalCmdNodeTool, SystemInfoNodeTool, ChangeDirectoryNodeTool

# Agents Nodes
class ShyamPlannerNode:
    def __init__(self, llm_provider: str = "groq"):
        self.llm_provider = llm_provider
        self.llm = LLMFactory.create_llm(llm_provider)
        self.tools = [WebSearchTool(), SaveMarkdownTool()]
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", Prompts.plannernode),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        )
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    def process(self, state: HeraPheriState) -> Dict[str, Any]:
        """Process the state for ShyamPlannerNode."""
        try:
            response = self.agent_executor.invoke({
                "input": state.task,
            })
            state.agent_output = response['output']
            
            state.node_type = "ShyamPlannerNode"
        
            return {
                "state": state,
                "output": response['output'],
                "success": True
            }
        except Exception as e:
            state.agent_output = f"Error in ShyamPlannerNode: {str(e)}"
            state.node_type = "ShyamPlannerNode"
            return {
                "response": state.agent_output,
                "node_type": state.node_type,
                "success": False,
                "error": str(e)
            }
    
class TaskPlannerNode:
    def __init__(self, llm_provider: str = "groq"):
        self.llm_provider = llm_provider
        self.llm = LLMFactory.create_llm(llm_provider)
        self.tools = [LoadMarkdownTool(), SaveMarkdownTool()]
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", Prompts.taskplannernode),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        )
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
    def process(self, state: HeraPheriState) -> Dict[str, Any]:
        """Process the state for TaskPlannerNode."""
        try:
            response = self.agent_executor.invoke({
                "input": state.agent_input,
            })
            state.agent_output = response['output']
            state.agent_input = state.agent_output
            state.node_type = "TaskPlannerNode"
            
            return {
                "state": state,
                "output": response['output'],
                "success": True
            }
        except Exception as e:
            state.agent_output = f"Error in TaskPlannerNode: {str(e)}"
            state.node_type = "TaskPlannerNode"
            return {
                "response": state.agent_output,
                "node_type": state.node_type,
                "success": False,
                "error": str(e)
            }
    
class RajuCoderNode:
    def __init__(self, llm_provider: str = "groq"):
        self.llm_provider = llm_provider
        self.llm = LLMFactory.create_llm(llm_provider)
        self.tools = [CreateFileTool(), UpdateFileTool()]
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", Prompts.rajucodernode),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        )
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
    def process(self, state: HeraPheriState) -> Dict[str, Any]:
        """Process the state for RajuCoderNode."""
        try:
            response = self.agent_executor.invoke({
                "input": state.agent_input,
            })
            state.agent_output = response['output']
            state.agent_input = state.agent_output
            state.node_type = "RajuCoderNode"
            
            return {
                "state": state,
                "output": response['output'],
                "success": True
            }
        except Exception as e:
            state.agent_output = f"Error in RajuCoderNode: {str(e)}"
            state.node_type = "RajuCoderNode"
            return {
                "response": state.agent_output,
                "node_type": state.node_type,
                "success": False,
                "error": str(e)
            }
    
class ShyamReviewerNode:
    def __init__(self, llm_provider: str = "groq"):
        self.llm_provider = llm_provider
        self.llm = LLMFactory.create_llm(llm_provider)
        self.tools = [WebSearchTool()]
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", Prompts.shyamreviewernode),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        )
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
    def process(self, state: HeraPheriState) -> Dict[str, Any]:
        """Process the state for ShyamReviewerNode."""
        try:
            response = self.agent_executor.invoke({
                "input": state.agent_input,
            })
            state.agent_output = response['output']
            state.agent_input = state.agent_output
            state.node_type = "ShyamReviewerNode"
            
            return {
                "state": state,
                "output": response['output'],
                "success": True
            }
        except Exception as e:
            state.agent_output = f"Error in ShyamReviewerNode: {str(e)}"
            state.node_type = "ShyamReviewerNode"
            return {
                "response": state.agent_output,
                "node_type": state.node_type,
                "success": False,
                "error": str(e)
            }
    
class BabuBhiyaNode:
    def __init__(self, llm_provider: str = "groq"):
        self.llm_provider = llm_provider
        self.llm = LLMFactory.create_llm(llm_provider)
        self.tools = [TerminalCmdNodeTool(), SystemInfoNodeTool(), ChangeDirectoryNodeTool()]
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", Prompts.babubhaiyanode),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        )
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
    def process(self, state: HeraPheriState) -> Dict[str, Any]:
        """Process the state for BabuBhaiyaNode."""
        try:
            response = self.agent_executor.invoke({
                "input": state.agent_input,
            })
            state.agent_output = response['output']
            state.agent_input = state.agent_output
            state.node_type = "BabuBhaiyaNode"
            
            return {
                "state": state,
                "output": response['output'],
                "success": True
            }
        except Exception as e:
            state.agent_output = f"Error in BabuBhaiyaNode: {str(e)}"
            state.node_type = "BabuBhaiyaNode"
            return {
                "response": state.agent_output,
                "node_type": state.node_type,
                "success": False,
                "error": str(e)
            }