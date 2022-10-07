from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="API REST Products",
        description="Test backend for Zebrand",
        version="1.0",
        terms_of_service="",
        contact={
            "name": "Gerardo Cunya",
            "url": "https://github.com/victorcunya",
            "email": "cunya.victor@gmail.com",
        },
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    return app;
