from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column, DeclarativeBase
from passlib.context import CryptContext
import os

class Base(DeclarativeBase):
    pass

DATABASE_URL = "sqlite:///./sql_app.db"
# Ajustado para usar check_same_thread=False, necessário para SQLite em apps async/multi-thread (FastAPI)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Password Hashing ---
# O bcrypt tem o limite de 72 bytes, por isso a truncagem é essencial.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Models ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

app = FastAPI()

# --- Utility Functions ---

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# --- Endpoints ---
@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Usa a função corrigida
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login_for_access_token(user_login: UserLogin, db: Session = Depends(get_db)):
    user = get_user(db, email=user_login.email)
    
    # Usa a função corrigida
    if not user or not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Em uma aplicação real, você geraria um token JWT aqui.
    return {"message": "Login successful", "user": user.email}

if __name__ == "__main__":
    import uvicorn
    # Não inclua o uvicorn.run aqui se o arquivo for executado dentro de um ambiente de container/runtime,
    # mas mantenho para fins de demonstração local.
    uvicorn.run(app, host="0.0.0.0", port=8000)