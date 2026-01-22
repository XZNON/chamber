from langgraph.graph import StateGraph,START,END
from models.chamber_state import ChamberState
from core.reasoner import reasoner
from core.orchestrator import orchestrator
from core.decomposer import decomposer
from core.executor import executePlan
from utils.decomposer_router import decomposer_router
from dotenv import load_dotenv
from core.logger import get_logger

load_dotenv()

logger = get_logger("Chamber Graph")


#########################################Graph Building########################################################

chamberGraphStruct = StateGraph(ChamberState) 

chamberGraphStruct.add_node('reasoner',reasoner)
chamberGraphStruct.add_node('orchestrator',orchestrator)
chamberGraphStruct.add_node('decomposer',decomposer)
chamberGraphStruct.add_node('executioner',executePlan)


chamberGraphStruct.add_edge(START,'reasoner')
chamberGraphStruct.add_edge('reasoner','orchestrator')
chamberGraphStruct.add_conditional_edges('orchestrator',decomposer_router)
chamberGraphStruct.add_edge('decomposer','orchestrator')
chamberGraphStruct.add_edge('executioner',END)

chamberGraph = chamberGraphStruct.compile()

print(chamberGraph.get_graph().draw_mermaid())