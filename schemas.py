
from pydantic import BaseModel,Field
from typing import Optional,TypeVar,Generic

class Address(BaseModel):
  address1 : str
  address2: str
  address3: Optional[str]
  kana1: str
  kana2: str
  kana3: Optional[str]
  prefcode: str
  zipcode: str = Field(max_length=7,min_length=7)

T = TypeVar('T')

class ItemResponse(BaseModel,Generic[T]):
  message: str
  result: Optional[T] = None
  status : int
