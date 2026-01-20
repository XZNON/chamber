#decomposer node
from models.chamber_state import ChamberState
from core.logger import get_logger
from dataclasses import dataclass

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

    decomposeablePlan = []

    if executablePlan:
        for idx,goal in enumerate(executablePlan):
            if goal['need_decomposition']:
                # send the goal to the LLM to further get decomposed into atomic sub-goals

                #sample outpur for the LLM call
                subGoals =  [
                    Goal(description='Create API route for product listing'),
                    Goal(description='Create API route for order placement'),
                    Goal(description='Create API route for user registration'),
                    Goal(description='Create API route for login')
                ]

                newGoals = (
                    goals[:idx] + subGoals + goals[idx+1:]
                )

            return {
                'goals' : newGoals
            }
    return state
                    
@dataclass
class Goal:
    description : str

@dataclass
class ReasonerOutputSchema:
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
    print(json.dumps(
        {"goals": [g.description for g in result["goals"]]},
        indent=2
    ))


#used to decompose vague/large goals into small atomic executable goals for the executioner

#if a decomposable goal shows up from the decomposer router(implement), it splits that goal into atomic chunk size goals to execute
# sends the goals back to the orchestrator