
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '15d60a651185b10db6f08b196bc87afd75a1867a4403f1ec4a3f4e83c532def1'
ALGORITHM = 'HS256'


def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
        return pwd_context.hash(password)

def encode_jwt(to_encode: dict):
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
