
from dependency_injector import containers, providers

from app.config import settings
from app.core.service.product import ProductService
from app.core.service.tracking import TrackingService
from app.core.service.user import UserService
from app.infrastructure.adapters.postgres import Database
from app.infrastructure.adapters.postgres.product import ProductDB
from app.infrastructure.adapters.postgres.tracking import TrackingDB
from app.infrastructure.adapters.postgres.user import UserDB
from app.infrastructure.adapters.rest.mail import MailSMTPAdapter


class Container(containers.DeclarativeContainer):

    db = providers.Singleton(
        Database,
        db_url=settings.DATABASE_URL
    )
    product_repository = providers.Factory(
        ProductDB,
        session=db.provided.session
    )
    product_service = providers.Factory(
        ProductService,
        product_repository=product_repository,
        mail_repository=MailSMTPAdapter(),
    )
    user_repository = providers.Factory(
        UserDB,
        session=db.provided.session
    )
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
    tracking_repository = providers.Factory(
        TrackingDB,
        session=db.provided.session
    )
    tracking_service = providers.Factory(
        TrackingService,
        tracking_repository=tracking_repository,
    )
