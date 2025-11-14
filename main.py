# main.py
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from database import Base, engine
from models import User
from routers import orderes, pizzas, users

# Create app once
app = FastAPI(title="Pizza Delivery API")

# Security scheme
security = HTTPBearer()

@app.get("/secure-data")
def secure_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {"token": credentials.credentials, "msg": "You are authenticated"}

# 👇 Custom Swagger to show "Bearer Token"
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Pizza Delivery API",
        version="1.0.0",
        description="API for pizza ordering",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Create tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(users.router)
app.include_router(pizzas.router)
app.include_router(orderes.router)



# # main.py
# from fastapi import FastAPI
# from database import Base, engine
# from models import User
# from routers import pizzas, users
# from fastapi import FastAPI, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from fastapi.openapi.utils import get_openapi

# # Create app
# app = FastAPI()

# # Security scheme
# security = HTTPBearer()

# # Example secured endpoint
# @app.get("/secure-data")
# def secure_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     return {"token": credentials.credentials, "msg": "You are authenticated"}

# # 👇 Custom Swagger to show "Bearer Token"
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Pizza Delivery API",
#         version="1.0.0",
#         description="API for pizza ordering",
#         routes=app.routes,
#     )
#     openapi_schema["components"]["securitySchemes"] = {
#         "BearerAuth": {
#             "type": "http",
#             "scheme": "bearer",
#             "bearerFormat": "JWT",
#         }
#     }
#     for path in openapi_schema["paths"].values():
#         for method in path.values():
#             method["security"] = [{"BearerAuth": []}]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi






# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Pizza Delivery API")

# # Routers
# app.include_router(users.router)
# app.include_router(pizzas.router)
