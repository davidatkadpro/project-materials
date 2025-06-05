from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class Material(BaseModel):
    id: int
    name: str
    unit: str
    notes: Optional[str] = None


class Supplier(BaseModel):
    id: int
    name: str
    contact: Optional[str] = None
    materials: List[int] = []


class Service(BaseModel):
    id: int
    name: str
    unit_price: float
    notes: Optional[str] = None


class Quote(BaseModel):
    id: int
    project_id: int
    supplier_id: int
    material_id: Optional[int] = None
    service_id: Optional[int] = None
    quantity: float
    price: float


class OrderStatus(str, Enum):
    pending = "pending"
    ordered = "ordered"
    completed = "completed"


class Order(BaseModel):
    id: int
    quote_id: int
    status: OrderStatus = OrderStatus.pending
    final_price: Optional[float] = None

