from typing import Optional
from pydantic import BaseModel

class ReviewRequest(BaseModel):
    diff:str
    language:str
    context:str|None=None

