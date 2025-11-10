from typing import TypedDict,Optional,List,Annotated
from langgraph.graph.message import add_messages

class ChamberState(TypedDict):
    input : Annotated[list[str],add_messages] 
    plan : Optional[List[dict]]
    error : Optional[str]
    metadata : Optional[dict]
    result : Optional[List[dict]]

