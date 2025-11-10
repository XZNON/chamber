from pydantic import BaseModel,Field
from typing import List,Optional

class ShellCommandSchema(BaseModel):
    cmd : str = Field(...,description="The base shell command to execute, eg: npm, git,pip, etc")
    arg : Optional[List[str]] = Field(default_factory=list,description="List of command arguments")
    cwd : Optional[str] = Field(None,description="Optional directory to run the command in")
    captureOutput : bool = Field(default=True,description="Weather you want to capture the command output")
    shell : bool = Field(default=True, description="run using shell=True for system commands")