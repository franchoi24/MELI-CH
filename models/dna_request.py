from typing import Optional
from pydantic import BaseModel

class DnaRequest(BaseModel):
    dna: list[str]
    recursive: Optional[bool] = None