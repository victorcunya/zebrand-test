from contextlib import AbstractAsyncContextManager
from typing import Callable

from app.core.repository.tracking import TrackingRepository
from app.core.schema.tracking import Tracking, TrackingBase
from sqlalchemy.orm import Session

from .models import Tracking as TrackingModel


class TrackingDB(TrackingRepository):

    def __init__(self, session: Callable[..., AbstractAsyncContextManager[Session]]) -> None:
        self._session_factory = session

    def create(self, data: TrackingBase) -> Tracking:
        with self._session_factory() as session:
            tracking = TrackingModel(**data.dict())
            session.add(tracking)
            session.commit()
            session.refresh(tracking)
            return Tracking.from_orm(tracking)
