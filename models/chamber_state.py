from typing import TypedDict,Optional,List,Annotated

def mergeLists(a : list,b : list) -> list:
    return a+b

class ChamberState(TypedDict):
    input : Annotated[list[str],mergeLists] 
    goals : Annotated[list[dict],mergeLists]
    execution_plan : Annotated[List[dict],mergeLists]
    workspace : dict
    error : Optional[str]
    metadata : Optional[dict]
    result : Optional[List[dict]]

