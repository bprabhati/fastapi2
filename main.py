from fastapi import FastAPI,HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schema import UserCreate, UserUpdate 
import uvicorn
from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def hello_world():
    data={"message":"Hello from FastAPI"}
    return JSONResponse(content=data,status_code=200)

@app.get("/users")
def get_all_users(db: Session=Depends(get_db)):
    return db.query(User).all()


@app.get("users/{user_id}")
def get_user_by_email(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, details="User not found")

@app.post("/users")
def create_user(user: UserCreate, db: Session =Depends(get_db)):
    db_user = User(name=user.name, age=user.age, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}")
def update_user_by_email(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}")
def delete_user_by_email(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

if __name__ =="__main__":
    uvicorn.run(app, host="127.0.0.1",port=8000)
