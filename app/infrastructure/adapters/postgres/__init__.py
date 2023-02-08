
import logging
from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session, declarative_base

logger = logging.getLogger(__name__)
Base = declarative_base()

class Database:

    def __init__(self, db_url) -> None:
        self._engine = create_engine(db_url)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                expire_on_commit=False
            )
        )

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory
        try:
            yield session
        except Exception:
            logger.exception('Session rollback')
            session.rollback()
            raise
        finally:
            session.close()
