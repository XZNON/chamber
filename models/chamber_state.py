from typing import TypedDict,Optional,List,Annotated
from operator import add
from workspace.workspace_manager import WorkspaceManager

def mergeLists(a : list,b : list) -> list:
    return a+b

class ChamberState(TypedDict):
    input : Annotated[list[str],add] 
    goals : list[dict]
    currentGoalIdx : int = 0
    workspace : WorkspaceManager
    error : Optional[str] | None

