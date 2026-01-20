from models.chamber_state import ChamberState
from utils.domain_classifier import classifyDomains
from utils.decompostion_heuristic import heuristicNeedsDecomposition
from core.logger import get_logger

#########################   testing libraries  #########################
from dataclasses import dataclass

logger = get_logger("Orchestrator")

def orchestrator(state : ChamberState) -> ChamberState:
    goals = state.get('goals',[])
    descriptions = [g.description for g in goals]

    try:
        domainAndDecomposition = classifyDomains(goals)
        logger.info("Orchestrator generated domains successfully")
    except Exception as e:
        logger.error(f"Reasoner Failed: {e}")
        return {
            "error":str(e),
            "metadata":{
                "source":"reasoner_[classifyDomains]",
                "status":"failed"
            }
        }


    executionPlan = []

    #each goal will have its execution step, it should have a {domain, intent, requires_decomposition}
    for i in range(len(goals)):
        try:
            needDecom = heuristicNeedsDecomposition(goals[i].description) or domainAndDecomposition[i]['needs_decomposition']
            executionPlan.append({
                "domain" : domainAndDecomposition[i]["domain"],
                "intent" : descriptions[i],
                "need_decomposition" : needDecom,
                "status" : "pending"
            })
        except Exception as e:
            
            logger.error(f"Reasoner Failed: {e}")
            return {
                "error":str(e),
                "metadata":{
                    "source":"reasoner_[executionPlans]",
                    "status":"failed"
            }
            }
    
    logger.info("Orchestrator generated plans successfully")

    return {
        'execution_plan' : executionPlan
    }


################################################################################################################################################
##############################################################     Testing      ################################################################ 
################################################################################################################################################


@dataclass
class Goal:
    description : str

if __name__ == "__main__":
    mock_goals = [
        Goal(description='Define the project folder structure'),
        Goal(description='Define database models for shoes'),
        Goal(description='Add styling and user interface polish to ensure a smooth and attractive user experience'),
        Goal(description='Build UI components for shopping cart'),
        Goal(description='Create API routes to support core e-commerce functionalities like product listing, user registration, login, and order placement')
    ]

    dummyState = {
        'input': ["Create a shoe store"],
        'goals': mock_goals,
        'workspace': {},
        'execution_plan': []
    }
    
    print("--- Running Orchestrator Test ---")
    result = orchestrator(dummyState)

    import json
    print(json.dumps(result, indent=2))
    
    assert len(result['execution_plan']) == len(mock_goals)
    print("\nTest Passed: Execution plan matches goal count.")

# {'goals': [Goal(description='Define the project folder structure for the full stack e-commerce website'),
#  Goal(description='Set up the backend service to handle product data, user management, and order processing'),
#  Goal(description='Define database models for shoes, users, orders, and any other required entities'),
#  Goal(description='Create API routes to support core e-commerce functionalities like product listing, user registration, login, and order placement'),
#  Goal(description='Set up the frontend application to present the user interface for browsing and purchasing shoes'), 
# Goal(description='Build user interface components for product display, shopping cart, user authentication, and checkout'),
#  Goal(description='Add styling and user interface polish to ensure a smooth and attractive user experience')
# ], 'error': None, 'metadata': {'model': 'gpt-4o-mini', 'source': 'reasoner'}}