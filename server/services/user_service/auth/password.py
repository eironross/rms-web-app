from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt", "argon2"], default="argon2", deprecated="auto")

def hash_password(password: str) -> str:
    return context.hash(password)

def check_password(password: str, hashed_password: str) -> bool:
    return context.verify(password, hashed_password)