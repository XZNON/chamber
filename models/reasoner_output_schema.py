from pydantic import BaseModel,Field
from typing import Dict,List,Any

class PlanStep(BaseModel):
    action : str = Field(description="The tool to be used, eg: 'create_file','delete_file','shell_execute' ")
    params : Dict[str,Any] = Field(description="The parameters for the action, E.g: {'path':'...','content':'...'} or {'cmd':'...','arg':[...]}")

class ReasonerOutputSchema(BaseModel):
    plan : List[PlanStep] = Field(description="a list of structured steps defining the execution plan")