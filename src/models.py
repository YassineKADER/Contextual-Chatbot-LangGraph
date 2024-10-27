from pydantic import BaseModel
from typing import List


# FastAPI models
class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str
    steps: List[str]
