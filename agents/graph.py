from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, END
from database.storage import ConversationStorage
from database.models import Conversation
import uuid
from agents.state import HeraPheriState
from agents.nodes import (
    ShyamPlannerNode,
    TaskPlannerNode,
    RajuCoderNode,
    ShyamReviewerNode,
    BabuBhiyaNode,
)

class HeraPheriGraph(StateGraph):
    def __init__(self, llm_provider: str = "groq", session_id: str = None):
        self.llm_provider = llm_provider
        self.session_id = session_id or uuid.uuid4().hex
        self.storage = ConversationStorage()
        
        # Init nodes
        self.planning_node = ShyamPlannerNode(llm_provider=self.llm_provider)
        self.task_planner_node = TaskPlannerNode(llm_provider=self.llm_provider)
        self.raju_coder_node = RajuCoderNode(llm_provider=self.llm_provider)
        self.shyam_reviewer_node = ShyamReviewerNode(llm_provider=self.llm_provider)
        self.babu_bhiya_node = BabuBhiyaNode(llm_provider=self.llm_provider)
        
        # Build graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the state graph for HeraPheri agents."""
        
        graph = StateGraph(dict)
        
        # Add all nodes
        graph.add_node("Shyam Planner", self._planner_node_wrapper)
        graph.add_node("Raju coder", self._raju_coder_node_wrapper)
        graph.add_node("Shyam Review", self._shyam_reviewer_node_wrapper)
        graph.add_node("Babu Bhaiya", self._babu_bhaiya_node_wrapper)
        graph.add_node("Task Remaining", lambda state: state)
        
        graph.add_edge("Shyam Planner", "Task Remaining")
        graph.add_edge("Shyam Review", "Raju coder")
        graph.add_edge("Raju coder", "Babu Bhaiya")
        
        graph.add_conditional_edges(
            "Task Remaining",
            self._task_remaining_node,
            {
                "__else__": "Raju coder",
                "END": END
            }
        )

        graph.add_conditional_edges(
            "Babu Bhaiya",
            self._babu_bhaiya_routing,
            {
                "Success": "Task Remaining",
                "Error": "Shyam Review"
            }
        )
        graph.set_entry_point("Shyam Planner")
        
        return graph.compile()
    
    def _planner_node_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper of planner node"""
        agent_state = HeraPheriState()
        agent_state.task = state['task']
        agent_state.agent_input = state['task']
        agent_state.llm_provider = self.llm_provider
        agent_state.session_id = self.session_id
        
        result = self.planning_node.process(agent_state)
        
        conversation = Conversation(
            session_id=self.session_id,
            node_type="ShyamPlannerNode",
            messages=[
                f"Input: {agent_state.task}",
                f"Output: {result['output']}"
            ],
            llm_provider=self.llm_provider
        )
        
        self.storage.create(conversation)
        
        return {
            **state,
            "agent_input": result['output'],
            "response": result['output'],
            "node_type": "ShyamPlannerNode",
            "success": result['success'],
        }
        
    def _raju_coder_node_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for Raju Coder Node"""
        agent_state = HeraPheriState()
        agent_state.agent_input = state.get('agent_input', '')
        agent_state.llm_provider = self.llm_provider
        agent_state.session_id = self.session_id
        
        result = self.raju_coder_node.process(agent_state)
        
        conversation = Conversation(
            session_id=self.session_id,
            node_type="RajuCoderNode",
            messages=[
                f"Input: {agent_state.agent_input}",
                f"Output: {result['output']}"
            ],
            llm_provider=self.llm_provider
        )
        
        self.storage.create(conversation)
        
        return {
            **state,
            "agent_input": result['output'],
            "response": result['output'],
            "node_type": "RajuCoderNode",
            "success": result['success'],
        }
        
    def _shyam_reviewer_node_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for Shyam Reviewer Node"""
        agent_state = HeraPheriState()
        agent_state.agent_input = state.get('agent_input', '')
        agent_state.llm_provider = self.llm_provider
        agent_state.session_id = self.session_id
        
        result = self.shyam_reviewer_node.process(agent_state)
        
        conversation = Conversation(
            session_id=self.session_id,
            node_type="ShyamReviewerNode",
            messages=[
                f"Input: {agent_state.agent_input}",
                f"Output: {result['output']}"
            ],
            llm_provider=self.llm_provider
        )
        
        self.storage.create(conversation)
        
        return {
            **state,
            "agent_input": result['output'],
            "response": result['output'],
            "node_type": "ShyamReviewerNode",
            "success": result['success'],
        }
        
    def _babu_bhaiya_node_wrapper(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for Babu Bhaiya Node"""
        agent_state = HeraPheriState()
        agent_state.agent_input = state.get('agent_input', '')
        agent_state.llm_provider = self.llm_provider
        agent_state.session_id = self.session_id
        
        result = self.babu_bhiya_node.process(agent_state)
        
        conversation = Conversation(
            session_id=self.session_id,
            node_type="BabuBhiyaNode",
            messages=[
                f"Input: {agent_state.agent_input}",
                f"Output: {result['output']}"
            ],
            llm_provider=self.llm_provider
        )
        
        self.storage.create(conversation)
        
        return {
            **state,
            "agent_input": result['output'],
            "response": result['output'],
            "node_type": "BabuBhiyaNode",
            "success": result['success'],
        }
        
    def _babu_bhaiya_routing(self, state: Dict[str, Any]) -> Literal["Success", "Error"]:
        """Route based on Babu Bhaiya node success/failure"""
        return "Success" if state.get('success', False) else "Error"
        
    def _task_remaining_node(self, state: Dict[str, Any]) -> Literal["__else__", "END"]:
        """Determine if there are more tasks remaining."""
        agent_state = HeraPheriState()
        agent_state.agent_input = state.get('agent_input', '')
        agent_state.llm_provider = self.llm_provider
        agent_state.session_id = self.session_id
        
        result = self.task_planner_node.process(agent_state)
        
        # Check if any completion phrases are in the output
        completion_phrases = ['all tasks are completed', 'end', 'sucessfully completed all the tasks']
        output_lower = result['output'].lower()
        
        if any(phrase in output_lower for phrase in completion_phrases):
            return "END"
        else:
            conversation = Conversation(
                session_id=self.session_id,
                node_type="TaskPlannerNode",
                messages=[
                    f"Input: {agent_state.agent_input}",
                    f"Output: {result['output']}"
                ],
                llm_provider=self.llm_provider
            )
            self.storage.create(conversation)
            
            # Update state for next node
            state.update({
                "agent_input": result['output'],
                "response": result['output'],
                "node_type": "TaskPlannerNode",
                "success": result['success'],
            })
            
            return "__else__"
            
        
    def process_input(self, initial_state: str) -> Dict[str, Any]:
        """Process the initial input through the state graph."""
        initial_input = {
            "task": initial_state,
            "session_id": self.session_id,
        }
        
        result = self.graph.invoke(initial_input)
        return result