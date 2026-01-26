from models.chamber_state import ChamberState
from utils.domain_classifier import classifyDomains
from core.logger import get_logger
from utils.route_executioner import routeExecutioner
#########################   testing libraries  #########################
from dataclasses import dataclass

logger = get_logger("Orchestrator")

def orchestrator(state : ChamberState) -> ChamberState:
    goals = state.get('goals',[])
    idx = state.get('currentGoalIdx')

    print(goals)
    # if idx >= len(goals):
    #     logger.info("All goals completed")
    #     return state


    #get the current goal
    goal = goals[idx]
    logger.info(f"Starting goal {idx+1}/{len(goals)} : {goal.description}")

    goal.status = "running"
    # print(goal,goals)
    try:
        #route the goal to the executioner
        executioner = routeExecutioner(goal.description)

        if executioner is None:
            raise RuntimeError(f"No goal executioner found for goal : {goal.description}")
        
        executioner.execute(goal,state)

        goal.status = "done"
        logger.info(f"Completed goal: {goal.description}")

    except Exception as e:
        goal.status = 'failed'
        state['error'] = str(e)
        logger.error(f"Goal Failed at orchestrator: {e}")
        return state

    state['currentGoalIdx'] += 1
    return state


################################################################################################################################################
##############################################################     Testing      ################################################################ 
################################################################################################################################################


if __name__ == "__main__":
    from models.reasoner_output_schema import Goal

    state = {
        "input": ["Build something"],
        "goals": [
            Goal(description="Define project structure"),
            Goal(description="Implement backend"),
        ],
        "currentGoalIdx": 0,
        "workspace": {},
        "error": None
    }

    while state["currentGoalIdx"] < len(state["goals"]):
        state = orchestrator(state)