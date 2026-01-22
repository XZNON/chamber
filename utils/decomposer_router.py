from models.chamber_state import ChamberState
from typing import Literal
from core.logger import get_logger

logger = get_logger("Decomposer Router")

def decomposer_router(state : ChamberState) -> Literal['decomposer','executioner']:

    executionPlan = state.get('execution_plan',[])
    depth = state.get('decomposition_depth',0)

    print(depth)

    #should i have guard-rails? and how much?
    #test tomorrow
    if depth >= 3:
        logger.info('Decomposition depth reached')
        return 'executioner'
    
    for plan in executionPlan:
        if plan.get('need_decomposition',False):
            logger.info('Plan found that needs decomposition, routing to decomposer')
            return 'decomposer'
    
    logger.info('no plan found that needs decomposition, routing to executioner')
    return 'executioner'
