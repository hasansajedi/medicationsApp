from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


class BaseListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]


class DrugModel(BaseModel):
    id: str
    diseases: List[str]
    description: str
    name: Optional[str]
    released: str

    @field_validator("released")
    def set_released(cls, released):
        if released:
            input_date = datetime.strptime(released, "%Y-%m-%d")
            return input_date.strftime("%d/%m/%Y")


class DrugListResponse(BaseListResponse):
    results: List[Optional[DrugModel]]
