from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace password with your MySQL root password
DATABASE_URL = "mysql+pymysql://root:Nissu%400702@localhost:3306/test_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()