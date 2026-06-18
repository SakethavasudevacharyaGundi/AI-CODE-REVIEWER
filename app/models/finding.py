from typing import Literal
from pydantic import BaseModel

class Finding(BaseModel):
    id:str|None=None
    line:int|None=None  
    line_content:str
    category:Literal["security", "performance", "correctness", "style", "test_coverage"]
    severity:Literal["low", "medium", "high","critical"]
    title:str
    description:str
    suggestion:str