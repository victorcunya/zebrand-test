
from app.config import settings
from app.core.service.product import ProductService
from app.infrastructure.adapters.postgres import Database
from app.infrastructure.adapters.postgres.product import ProductDB
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
