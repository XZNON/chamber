from pydantic import BaseModel,ConfigDict

class chamberBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,extra='ignore')