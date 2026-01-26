from langgraph.graph import StateGraph,START,END
from models.chamber_state import ChamberState
from core.reasoner import reasoner
from core.orchestrator import orchestrator
from core.decomposer import decomposer
from core.executor import executioner
from dotenv import load_dotenv
from core.logger import get_logger
import json

load_dotenv()

logger = get_logger("Chamber Graph")


#########################################Graph Building#####################################################

chamberGraphStruct = StateGraph(ChamberState) 

chamberGraphStruct.add_node('reasoner',reasoner)
chamberGraphStruct.add_node('orchestrator',orchestrator)
chamberGraphStruct.add_node('decomposer',decomposer)
chamberGraphStruct.add_node('executioner',executioner)


chamberGraphStruct.add_edge(START,'reasoner')
chamberGraphStruct.add_edge('reasoner','orchestrator')
chamberGraphStruct.add_conditional_edges(
    'orchestrator',decomposer_router,
    {
        'decomposer':'decomposer',
        'executioner' : 'executioner'
    }
    )
chamberGraphStruct.add_edge('decomposer','orchestrator')
chamberGraphStruct.add_edge('executioner',END)

chamberGraph = chamberGraphStruct.compile()


if __name__ == "__main__":
    input = ['create a frontend for my shoe selling store using react']

    res = chamberGraph.invoke({"input" : input})

    print(res)

    