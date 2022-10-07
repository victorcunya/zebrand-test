from fastapi import APIRouter

router = APIRouter(prefix='/api')

from .adapters.postgres import models  # noqa
