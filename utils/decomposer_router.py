from models.chamber_state import ChamberState
from typing import Literal
from core.logger import get_logger

logger = get_logger("Decomposer Router")

def decomposer_router(state : ChamberState) -> Literal['decomposer','executioner']:

    executionPlan = state.get('execution_plan',[])

    if not executionPlan:
        logger.error(f'No execution plan provided')
        return 'executioner'
    
    for plan in executionPlan:
        if plan.get('needs_decomposition',False):
            logger.info('Plan found that needs decomposition, routing to decomposer')
            return 'decomposer'
    
    logger.info('no plan found that needs decomposition, routing to executioner')
    return 'executioner'
