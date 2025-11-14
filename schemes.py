from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    role:str= "customer" 
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str



class PizzaBase(BaseModel):
    name: str
    size: str
    price: float

class PizzaCreate(PizzaBase):
    pass

class PizzaUpdate(BaseModel):
    name: Optional[str] = None
    size: Optional[str] = None
    price: Optional[float] = None
class PizzaResponse(PizzaBase):
    id: int

    class Config:
        orm_mode = True




class OrderPizza(BaseModel):
    pizza_id: int
    quantity: Optional[int] = 1  # optional for future extension

class OrderCreate(BaseModel):
    pizzas: List[OrderPizza]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float
    pizzas: List[int]  # List of pizza IDs
    created_at: datetime

    class Config:
        orm_mode = True