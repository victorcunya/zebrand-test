
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    from app.infrastructure import router
    app.include_router(router)

    @app.get('/')
    def root():
        return {
            "message": "Hello, world!"
        }

    return app
