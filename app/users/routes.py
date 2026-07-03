from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.users.schemas import (
    UserLoginSchema,
    UserRegisterSchema,
    UserResponseSchema,
    TokenSchema,
)
from app.users.models import UserModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.hasher import Hasher
from app.auth.jwt_auth import check_refresh_token
from app.services.jwt import create_access_token, create_refresh_token

router = APIRouter(tags=["users"], prefix="/users")


# LOGIN USER
@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(email=request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not Hasher.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    # access_token = create_access_token({"sub": str(user.id)})
    access_token = create_access_token({"user_id": str(user.id)})
    refresh_token = create_refresh_token({"user_id": str(user.id)})

    return JSONResponse(
        content={
            "detail": "user logged in successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


# REGISTER USER
@router.post("/register", response_model=UserResponseSchema, status_code=201)
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(email=request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user already exists"
        )
    hashed_password = Hasher.hash_password(request.password)
    user = UserModel(
        username=request.username, email=request.email, password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# REFRESH TOKEN
@router.post("/refresh-token")
async def refresh_token(request: TokenSchema, db: Session = Depends(get_db)):
    user_id = check_refresh_token(request.token)
    access_token = create_access_token({"user_id": str(user_id)})
    return JSONResponse(
        content={
            "detail": "refresh token accepted and access token issued",
            "access_token": access_token,
        }
    )
