from dataclasses import field
from typing import Any, Dict, Optional, List
from pydantic import BaseModel

class QAState(BaseModel):
    description:str
    requirement:Optional[str] = None
    test_case:Optional[str] = None
    automation_code: Optional[str] = None
    reviews: List[Dict[str, str]] = field(default_factory=list)
