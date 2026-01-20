from typing import TypedDict,Optional,List,Annotated

def mergeLists(a : list,b : list) -> list:
    return a+b

class ChamberState(TypedDict):
    input : Annotated[list[str],mergeLists] 
    goals : list[dict]
    execution_plan : Annotated[list[dict],mergeLists]
    workspace : dict
    error : Optional[str]
    metadata : Optional[dict]
    result : Optional[List[dict]]

