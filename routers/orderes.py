from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Order, Pizza
from auth import get_current_user
from schemes import OrderCreate, OrderResponse, OrderPizza

router = APIRouter(prefix="/orders", tags=["Orders"])

# Place an order (user only)
@router.post("/", response_model=OrderResponse)
def place_order(order: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only users can place orders")

    pizzas_in_order = db.query(Pizza).filter(Pizza.id.in_([p.pizza_id for p in order.pizzas])).all()
    if not pizzas_in_order:
        raise HTTPException(status_code=404, detail="No pizzas found")

    total_price = sum(p.price for p in pizzas_in_order)
    
    new_order = Order(user_id=current_user.id, total_price=total_price)
    new_order.pizzas = pizzas_in_order

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

     # ✅ Return data in format expected by OrderResponse
    return {
        "id": new_order.id,
        "user_id": new_order.user_id,
        "status": new_order.status,
        "total_price": new_order.total_price,
        "pizzas": [pizza.id for pizza in new_order.pizzas] , # Only return pizza IDs
        "created_at": new_order.created_at
    }

# Get all orders (admin only)
@router.get("/", response_model=List[OrderResponse])
def get_all_orders(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can view all orders")
    orders=db.query(Order).all()

    # Prepare response
    response = []
    for order in orders:
        order_data = {
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_price": order.total_price,
            "pizzas": [pizza.id for pizza in order.pizzas],  # only IDs
            "created_at": order.created_at
        }
        response.append(order_data)

    return response


# Update order status (admin only)
@router.put("/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update orders")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status
    db.commit()
    db.refresh(order)
    return order
