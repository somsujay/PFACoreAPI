from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name: str
    age: int
    city: str

class CrossTabRequest(BaseModel):
    accounts: List[str]
    markets: List[str]
    stocks: List[str]