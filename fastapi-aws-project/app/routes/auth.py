from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.jwt import create_access_token
from app.database.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = pwd_context.hash(
        user_data.password
    )

    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=Token
)
def login(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not pwd_context.verify(
        user_data.password,
        user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }