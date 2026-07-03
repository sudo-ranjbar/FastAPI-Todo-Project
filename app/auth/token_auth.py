from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.users.models import TokenModel
from app.core.database import get_db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.hasher import Hasher

security = HTTPBearer(scheme_name="Token")


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = db.query(TokenModel).filter_by(token=credentials.credentials).one_or_none()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    # other logics
    user = token.user
    return user
