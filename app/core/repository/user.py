
from abc import ABCMeta, abstractmethod

from app.core.schema.user import User, UserCreate, UserUpdate


class UserRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, data: UserCreate) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_user_by(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, data: UserUpdate) -> User:
        raise NotImplementedError
