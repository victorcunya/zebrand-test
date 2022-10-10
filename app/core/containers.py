
from app.config import settings
from app.core.service.product import ProductService
from app.core.service.tracking import TrackingService
from app.core.service.user import UserService
from app.infrastructure.adapters.postgres import Database
from app.infrastructure.adapters.postgres.product import ProductDB
from app.infrastructure.adapters.postgres.tracking import TrackingDB
from app.infrastructure.adapters.postgres.user import UserDB
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    db = providers.Singleton(
        Database,
        db_url=settings.DATABASE_URL
    )
    product_repo = providers.Factory(
        ProductDB,
        session=db.provided.session
    )
    product = providers.Factory(
        ProductService,
        repository=product_repo,
    )
    user_repo = providers.Factory(
        UserDB,
        session=db.provided.session
    )
    user = providers.Factory(
        UserService,
        repository=user_repo,
    )
    tracking_repo = providers.Factory(
        TrackingDB,
        session=db.provided.session
    )
    tracking = providers.Factory(
        TrackingService,
        repository=tracking_repo,
    )
