from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from typing import TypedDict
from core.config import GOOGLE_API_KEY,OPENAI_API_KEY
from core.executor import executePlan

def runPlan(state):
    plan = state.get("plan",[])
    result = executePlan(plan)
    return {
        'result':result
    }

graph = StateGraph(dict)
graph.add_node("runPlan",runPlan)

graph.add_edge(START,"runPlan")
graph.add_edge("runPlan",END)

compiled = graph.compile()
