#decomposer node
from models.chamber_state import ChamberState
from core.logger import get_logger
from dataclasses import dataclass
from utils.decompose_goals import decomposeGoal

logger = get_logger("Decomposer")

def decomposer(state : ChamberState) -> ChamberState:
    '''
    decomposer node:
        - Finds the first goal that needs decomposition
        - Replaces it with sub-goals 
        - Returns updated state 
        - will be send back to the orchestrator
        - Decomposes one goal at a time, safer, efficient
    '''

    executablePlan = state.get('execution_plan',[])
    goals = state.get('goals',[])


    if executablePlan:
        for idx,plan in enumerate(executablePlan):
            try:
                if plan['need_decomposition']:
                    intent = plan.get('intent','')

                    # send the plan to the LLM to further get decomposed into atomic sub-goals
                    if intent:     
                        subGoals = decomposeGoal(intent) # to-do
                    else:
                        continue
                        
                    #sample output for the LLM call
                    subGoals =  [
                        Goal(description='Create API route for product listing'),
                        Goal(description='Create API route for order placement'),
                        Goal(description='Create API route for user registration'),
                        Goal(description='Create API route for login')
                    ]

                    newGoals = (
                        goals[:idx] + subGoals + goals[idx+1:]
                    )

                logger.info("Decomposer added subGoals successfully")
                return {
                    'goals' : newGoals
                }
            except Exception as e:
                logger.error(f"Decomposer failed: {e}")
                return {
                    'error' : str(e),
                    'metadata' : {
                        "source":"decomposer_[subGoalAdditionLoop]",
                        "status":"failed"
                    }
                }
    return state
                    
@dataclass
class Goal:
    description : str

@dataclass
class GoalsSchema:
    goals : list[Goal] 
if __name__ == "__main__":
    execution_plan = [
        {
            "domain": "api",
            "intent": "Create API routes to support core e-commerce functionality",
            "need_decomposition": True,
            "status": "pending",
        }
    ]

    dummy_state = {
        "input": ["Create a shoe store"],
        "goals": [
            Goal(description="Create API routes to support core e-commerce functionality")
        ],
        "execution_plan": execution_plan,
        "workspace": {},
    }

    print("\n--- Running Decomposer Test ---")
    result = decomposer(dummy_state)

    import json
    # print(json.dumps(
    #     {"goals": [g.description for g in result["goals"]]},
    #     indent=2
    # ))


#used to decompose vague/large goals into small atomic executable goals for the executioner

#if a decomposable goal shows up from the decomposer router(implement), it splits that goal into atomic chunk size goals to execute
# sends the goals back to the orchestrator