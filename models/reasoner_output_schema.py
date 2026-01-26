from pydantic import BaseModel,Field
from typing import Dict,List,Any,Literal

GoalStatus = Literal['pending','running','done',' failed']

class Goal(BaseModel):
    description : str
    status : GoalStatus = 'pending'

class Goals(BaseModel):
    goals : List[Goal] = Field(description="a list of structured steps defining the plan")