# routers/pizzas.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Pizza, User
from schemes import PizzaCreate, PizzaResponse, PizzaUpdate
from typing import List
from auth import get_current_user

router = APIRouter(prefix="/pizzas", tags=["Pizzas"])

# ✅ Get all pizzas (anyone can see)
@router.get("/", response_model=List[PizzaResponse])
def get_pizzas(db: Session = Depends(get_db)):
    pizzas = db.query(Pizza).all()
    return pizzas

# ✅ Add pizza (Admin only)
@router.post("/", response_model=PizzaResponse)
def add_pizza(
    pizza: PizzaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add pizzas")
    
    new_pizza = Pizza(**pizza.dict())
    db.add(new_pizza)
    db.commit()
    db.refresh(new_pizza)
    return new_pizza

# ✅ Update pizza (Admin only)
@router.put("/{pizza_id}", response_model=PizzaResponse)
def update_pizza(
    pizza_id: int,
    pizza: PizzaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update pizzas")

    db_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    
    # ✅ Update only fields sent by client
    update_data = pizza.dict(exclude_unset=True)

    for key,value in update_data.items():
        setattr(db_pizza, key, value)

    db.commit()
    db.refresh(db_pizza)
    return db_pizza

# ✅ Delete pizza (Admin only)
@router.delete("/{pizza_id}")
def delete_pizza(
    pizza_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete pizzas")

    db_pizza = db.query(Pizza).filter(Pizza.id == pizza_id).first()
    if not db_pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")

    db.delete(db_pizza)
    db.commit()
    return {"message": "Pizza deleted successfully"}
