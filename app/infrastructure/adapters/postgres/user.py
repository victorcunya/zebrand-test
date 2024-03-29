
from contextlib import AbstractAsyncContextManager
from typing import Callable, Union

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.core.repository.user import UserRepository
from app.core.schema.user import User, UserRoleEnum

from .models import User as UserModel


class UserDB(UserRepository):

    def __init__(self, session: Callable[..., AbstractAsyncContextManager[Session]]) -> None:
        self._session_factory = session

    def create(self, data) -> User:
        try:
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
        except IntegrityError:
            return None

    def get_user_by(self, email) -> Union[User, None]:
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

    def update(self, pk, data) -> Union[User, None]:
        try:
            with self._session_factory() as session:
                user = session.query(UserModel).get(pk).update(**data.dict())
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
        except AttributeError:
            return None

    def delete(self, pk):
        try:
            with self._session_factory() as session:
                user = session.query(UserModel).get(pk).\
                    update(**{"state": 0})
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
        except Exception:
            return None
