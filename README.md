FastAPI Pizza Delivery API

A complete backend REST API for a Pizza Ordering System, built using FastAPI, MySQL, JWT Authentication, and SQLAlchemy ORM.
The system supports user registration, login, pizza management, order creation, and role-based access control.

🚀 Features
🔐 Authentication & Authorization

User registration & secure login

JWT-based authentication (Access Token)

Role-based permissions:

Admin → manage pizzas, manage orders

Customer → place orders, view own orders

🍕 Pizza Management (Admin Only)

Add new pizzas

Update pizza details

Delete pizzas

Fetch all pizzas (pagination supported)

🛒 Order Management

Customers can place orders

Each order can contain multiple pizzas

Admin can update order status → pending, delivered

Customers can view their orders

Admin can view all orders

🗄️ Database

MySQL + SQLAlchemy ORM

Auto table creation on startup

Relationships:

User → Orders

Order → Pizzas (many-to-many using association table)

🧪 Tech Stack

FastAPI (Python)

SQLAlchemy ORM

MySQL

JWT (PyJWT)

Pydantic

Uvicorn

bcrypt (password hashing)

📁 Project Structure
📦 fastapi-pizza-api
├── auth.py
├── database.py
├── main.py
├── models.py
├── routers
│   ├── pizzas.py
│   ├── orders.py
│   └── users.py
├── schemes.py
└── utils.py

🛠️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/yourusername/fastapi-pizza-api.git
cd fastapi-pizza-api

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure MySQL in database.py
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/pizza_db"

5️⃣ Run the server
uvicorn main:app --reload


Server will start at:
👉 http://127.0.0.1:8000

Swagger Docs:
👉 http://127.0.0.1:8000/docs

🔑 API Endpoints
👤 Auth Routes
Method	Endpoint	Description
POST	/users/register	Register new user
POST	/users/login	Login & get JWT token
🍕 Pizza Routes (Admin Only)
Method	Endpoint	Description
POST	/pizzas/	Create pizza
PUT	/pizzas/{id}	Update pizza
DELETE	/pizzas/{id}	Delete pizza
GET	/pizzas/	List pizzas
🛒 Order Routes
Method	Endpoint	Description
POST	/orders/	Place an order
GET	/orders/	Get user's orders / all orders (admin)
PUT	/orders/{id}/status	Update order status (admin)
📦 Example Request Bodies
➤ Register User
{
  "email": "user@example.com",
  "password": "password123"
}

➤ Login
{
  "email": "user@example.com",
  "password": "password123"
}

➤ Place Order
{
  "pizzas": [
    { "pizza_id": 1, "quantity": 2 }
  ]
}
