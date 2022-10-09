
from datetime import datetime, timedelta

from app.core.repository.user import UserRepository
from app.core.schema.user import Token, TokenData, User, UserCreate

from .utils.jwt import (decode_jwt, encode_jwt, get_password_hash,
                        verify_password)

ACCESS_TOKEN_EXPIRES_MINUTES = 30

class UserService:
    
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def create(self, data: UserCreate):
        data.password = get_password_hash(data.password)
        return self._repository.create(data)

    def get_user_by(self, email: str):
        return self._repository.get_user_by(email)

    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by(email)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: TokenData):
        delta = data.expire if data.expire else ACCESS_TOKEN_EXPIRES_MINUTES
        expire = datetime.utcnow() + timedelta(minutes=delta)
        to_encode={
            "sub": data.email,
            "exp": int(round(expire.timestamp()))
        }
        access_token = encode_jwt(to_encode)
        return Token(access_token=access_token, token_type="bearer")

    async def get_current_user(self, token: str) -> User:
        try:
            payload = decode_jwt(token)
            email = payload.get("sub")
            if email is None:
                return None
        except Exception:
            return None
        user = self.get_user_by(email)
        if user is None:
            return None
        return user
        
    