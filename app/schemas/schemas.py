# this file helps us to understand how data looks when it enters or leaves our API.

from pydantic import BaseModel, Field
from typing import Optional, List


class CustomerBase(BaseModel):
    customerName: str = Field(..., min_length=1, max_length=100)
    contactLastName: str = Field(..., min_length=1, max_length=100)
    contactFirstName: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., max_length=30)
    addressLine1: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)


class CustomerCreate(CustomerBase):
    pass    


class CustomerOut(CustomerBase):
    customerNumber: int
    orders: List[dict] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
