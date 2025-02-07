from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL="sqlite:///items.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the tables
Base.metadata.create_all(bind=engine) 