from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from models.auth_model import UserModel

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
print(f"Access tokens minutes: {type(ACCESS_TOKEN_EXPIRE_MINUTES)}")


class AuthService():
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt", "argon2"], default="argon2", deprecated="auto")
    
    async def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    async def check_password(self, password: str, hashed_password: str) -> bool:
        return self.context.verify(password, hashed_password)

    async def create_access_token(self, payload: UserModel) -> str:
        encode = {'sub': payload.email, "id": payload.id}
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        encode.update({"exp": expire})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    async def decode_access_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None