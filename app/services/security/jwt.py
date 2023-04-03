from datetime import datetime, timedelta
from typing import Optional, Dict, Union
from jose import jwt

from app.core.settings import settings


ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
) -> Dict[str, Union[str, datetime]]:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire,
                      "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY,
                             algorithm=ALGORITHM)
    return encoded_jwt


def generate_new_token(email: str) -> Dict[str, str]:
    """Generate new account token"""
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp,
         "nbf": now,
         "email": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_new_token(token: str) -> Optional[str]:
    """Verify the password reset token"""
    try:
        decoded_token = jwt.decode(token,
                                   settings.SECRET_KEY,
                                   algorithms=["HS256"])
        return decoded_token
    except jwt.JWTError:
        return None
