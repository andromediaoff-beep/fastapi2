from pydantic import BaseModel
from typing import Optional



class Movietop(BaseModel):
    name: str
    id: int
    cost: int
    director: str
    watched: bool
    file_path: Optional[str]
