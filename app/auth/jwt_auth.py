from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.users.models import UserModel
from app.core.database import get_db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from app.core.config import settings
from datetime import datetime, timezone

ALGORITHM = "HS256"
security = HTTPBearer(scheme_name="Token")


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Token Provided"
        )
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    token_type = decoded.get("type")
    exp_time = decoded.get("exp")
    user_id = decoded.get("user_id", None)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token Type"
        )
    if exp_time < datetime.now(timezone.utc).timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )
    # other logics
    user = db.query(UserModel).filter_by(id=user_id).one()
    return user


def check_refresh_token(token: str, db: Session = Depends(get_db)):
    """in this layer we cannot use db as dependency for getting the user.
    we get error so we just return user_id directly from the token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No Token Provided"
        )
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=ALGORITHM)
    token_type = decoded.get("type")
    exp_time = decoded.get("exp")
    user_id = decoded.get("user_id", None)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token Type"
        )
    if exp_time < datetime.now(timezone.utc).timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )
    # other logics
    # user = db.query(UserModel).filter_by(id=user_id).one()
    return user_id
