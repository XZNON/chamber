from pydantic import BaseModel,Field
from typing import Dict,List,Any

class Goal(BaseModel):
    description : str

class GoalsSchema(BaseModel):
    goals : List[Goal] = Field(description="a list of structured steps defining the plan")