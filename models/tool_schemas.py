from pydantic import BaseModel,Field
from typing import Optional

class FileInput(BaseModel):
    filename : str = Field(...,description="name of the file")
    path : Optional[str] = Field(default=".",description="Directory path where we want to create or write to a file")
    content : str = Field(...,description="Text content to write to the file")

class FileOutput(BaseModel):
    filename : str
    path : str
    status : str
    message : Optional[str] = None

class FileSchema(BaseModel):
    filename : str = Field(...,description="Name of the file to be deleted")
    path : Optional[str] = Field(default=".",description="Path of the file to be deleted")
