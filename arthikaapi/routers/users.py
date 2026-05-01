from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, Depends
from arthikaapi.schemas.users import NewUser, Login
from arthikaapi.utils.user_utils import hash_password
from arthikaapi.security.jwt_handler import create_access_token
from database import SessionLocal
from arthikaapi.models.users import User
from sqlalchemy.orm import Session
from arthikaapi.exceptions.custom_exceptions import UserExistsException


router = APIRouter(prefix="/api/arthika", tags=["User Operations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login(user: Login, db: Session = Depends(get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Check whether username exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid Username or Password")
    if not pwd_context.verify(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Password is wrong")
    access_token = create_access_token(data={"sub": existing_user.username})

    return {
    "access_token": access_token,
    "token_type": "bearer"
    }
    #return {"Result": "Login Successful"}
    


@router.post("/signup")
def signup(newuser: NewUser, db: Session = Depends(get_db)):
    print(f"User passed arguments are : {newuser.username}, {newuser.password}, {newuser.email}")
    try:
        # Check whether username exists
        existing_user = db.query(User).filter(User.username == newuser.username).first()
        if existing_user:
            raise UserExistsException(newuser.username)
        # create new user
        n_user = User(username=newuser.username, password=hash_password(newuser.password), 
                                email=newuser.email)
        db.add(n_user)
        db.commit()
        db.refresh(n_user)
    except UserExistsException as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while signup")
    return {"msg": "Signup Successful"}