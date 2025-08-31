from typing import Any, Dict, Optional
from pydantic import BaseModel

class QAState(BaseModel):
    description:str
    requirement:Optional[str] = None
    test_case:Optional[str] = None
    automation_code: Optional[str] = None
