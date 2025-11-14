from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="customer")

    # Back-reference to orders
    orders = relationship("Order", back_populates="user")


class Pizza(Base):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    size = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)


# Many-to-many relationship table
order_pizza = Table(
    "order_pizza",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("pizza_id", Integer, ForeignKey("pizzas.id"))
)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(50), default="pending")
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    pizzas = relationship("Pizza", secondary=order_pizza)



# from datetime import datetime
# from sqlalchemy import Column, DateTime, ForeignKey, Integer, String,Float, Table
# from database import Base
# from sqlalchemy.orm import relationship

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(100), unique=True, nullable=False)   # Added length
#     email = Column(String(120), unique=True, index=True, nullable=False)  # Added length
#     password = Column(String(255), nullable=False)  # store hashed password
#     role = Column(String(20), default="customer")   # e.g.


# class Pizza(Base):
#     __tablename__ = "pizzas"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), unique=True, index=True,nullable=False)
#     size = Column(String(20),nullable=False)   # Small, Medium, Large
#     price = Column(Float,nullable=False)



# # Many-to-many relationship between Order and Pizza
# order_pizza = Table(
#     "order_pizza",
#     Base.metadata,
#     Column("order_id", Integer, ForeignKey("orders.id")),
#     Column("pizza_id", Integer, ForeignKey("pizzas.id"))
# )

# class Order(Base):
#     __tablename__ = "orders"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     status = Column(String(50), default="pending")  # pending, preparing, delivered
#     total_price = Column(Float)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     user = relationship("User", back_populates="orders")
#     pizzas = relationship("Pizza", secondary=order_pizza)

# # Add back-reference in User model
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)
#     role = Column(String, default="user")

#     orders = relationship("Order", back_populates="user")