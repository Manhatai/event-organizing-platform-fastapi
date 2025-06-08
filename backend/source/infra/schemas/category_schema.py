from typing import Optional

from pydantic import BaseModel


class CategorySchema(BaseModel):
    categoryId: Optional[int] = None
    name: str
    value: int