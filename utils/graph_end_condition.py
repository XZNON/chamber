from models.chamber_state import ChamberState
from langgraph.graph import END

def shouldContinue(state : ChamberState):
    if state.get('error'):
        return END
    
    if state.get('currentGoalIdx') >= len(state.get('goals')):
        return END
    
    return 'orchestrator'