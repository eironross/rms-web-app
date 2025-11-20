from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
import os
from models.auth_model import UserModel

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

class AuthService():
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt", "argon2"], default="argon2", deprecated="auto")
    
    async def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    async def check_password(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)

    async def create_access_token(self, payload: UserModel, expires_delta: timedelta | None = None) -> str:
        to_encode = payload.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=365)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def decode_access_token(self, token: str) -> dict:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    