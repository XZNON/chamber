from models.chamber_state import ChamberState
from models.reasoner_output_schema import Goal

class BaseExecutioner:

    def can_handle(self,goalDescription : str) -> bool:
        raise NotImplementedError

    def execute(self,goal : Goal,state : ChamberState):
        raise NotImplementedError