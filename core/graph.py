from langgraph.graph import StateGraph,START,END
from models.chamber_state import ChamberState
from utils.graph_end_condition import shouldContinue
from core.reasoner import reasoner
from core.orchestrator import orchestrator
from dotenv import load_dotenv
from core.logger import get_logger
import json

load_dotenv()

logger = get_logger("Chamber Graph")




#########################################Graph Building#####################################################
def buildGraph():
    chamberGraphStruct = StateGraph(ChamberState) 

    chamberGraphStruct.add_node('reasoner',reasoner)
    chamberGraphStruct.add_node('orchestrator',orchestrator)


    chamberGraphStruct.add_edge(START,'reasoner')
    chamberGraphStruct.add_edge('reasoner','orchestrator')
    chamberGraphStruct.add_conditional_edges(
        "orchestrator",
        shouldContinue,
        {
            "orchestrator" : "orchestrator",
            END:END
        }
        )
    chamberGraph = chamberGraphStruct.compile()
    print(chamberGraph.get_graph().draw_mermaid())
    return chamberGraph

if __name__ == "__main__":
    app = buildGraph()

    initial_state = {
        "input": ["Build an Enigma machine and a website for me"],
        "goals": [],
        "current_goal_index": 0,
        "workspace": {},
        "error": None,
    }

    final_state = app.invoke(initial_state)

    print("\n=== FINAL STATE ===")
    for goal in final_state["goals"]:
        print(f"- {goal.description}: {goal.status}")
    