from pydantic import BaseModel,Field
from typing import Literal

DomainType = Literal[
    'structure',
    'database',
    'backend',
    'frontend',
    'ui',
    'api',
    'styling',
    'testing',
    'deployment',
    'code',
    'unknown'
]

class Domain(BaseModel):
    domain : DomainType = Field(description="The primary domain this goal belongs to.") 