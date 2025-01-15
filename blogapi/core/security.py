import logging
import secrets
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY: str = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
# 60 minutes * 24 hours * 7 days = 7 days
# ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
# ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def access_token_expire_minutes():
    return 30


# Create access token
def create_access_token(email: str):
    logger.debug("Creating access token", extra={"email": email})
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=access_token_expire_minutes()
    )
    jwt_data = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
