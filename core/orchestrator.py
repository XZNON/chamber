from models.chamber_state import ChamberState
from core.logger import get_logger

logger = get_logger("Orchestrator")

def orchestrator(state : ChamberState) -> ChamberState:
    goals = state.get('goals',[])

    executionPlan = []

    #each gaol will have its execution step, it should have a {domain, intent, requires_decomposition}
    for goal in goals:
        ...


# {'goals': [Goal(description='Define the project folder structure for the full stack e-commerce website'),
#  Goal(description='Set up the backend service to handle product data, user management, and order processing'),
#  Goal(description='Define database models for shoes, users, orders, and any other required entities'),
#  Goal(description='Create API routes to support core e-commerce functionalities like product listing, user registration, login, and order placement'),
#  Goal(description='Set up the frontend application to present the user interface for browsing and purchasing shoes'), 
# Goal(description='Build user interface components for product display, shopping cart, user authentication, and checkout'),
#  Goal(description='Add styling and user interface polish to ensure a smooth and attractive user experience')
# ], 'error': None, 'metadata': {'model': 'gpt-4o-mini', 'source': 'reasoner'}}