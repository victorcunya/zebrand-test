

from contextlib import AbstractAsyncContextManager
from typing import Callable

from app.core.repository.user import UserRepository
from app.core.schema.user import User, UserRoleEnum
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from .models import User as UserModel


class UserDB(UserRepository):

    def __init__(self, session: Callable[..., AbstractAsyncContextManager[Session]]) -> None:
        self._session_factory = session

    def create(self, data) -> User:
        with self._session_factory() as session:
            user = UserModel(
                email=data.email,
                name=data.name,
                password=data.password,
                role=data.role,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return User(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.password,
                role=UserRoleEnum(user.role.value),
                state=user.state
            )

    def get_user_by(self, email) -> User:
        try:
            with self._session_factory() as session:
                user = session.query(
                    UserModel.id,
                    UserModel.email,
                    UserModel.name,
                    UserModel.password,
                    UserModel.role,
                    UserModel.state,
                ).filter_by(email=email).one()
                return User(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.password,
                role=UserRoleEnum(user.role.value),
                state=user.state
            )
        except NoResultFound:
            return None

    def update(self, data) -> User:
        try:
            with self._session_factory() as session:
                session
        except Exception as e:
            raise e
