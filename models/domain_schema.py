from pydantic import BaseModel,Field
from typing import Literal,List

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
    domain : DomainType
    needs_decomposition : bool = False

class BatchClassifyDomain(BaseModel):
    results : List[Domain]