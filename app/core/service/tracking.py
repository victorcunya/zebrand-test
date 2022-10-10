
from app.core.repository.tracking import TrackingRepository


class TrackingService:

    def __init__(self, repository: TrackingRepository):
        self._repository = repository

    def create(self, data):
        return self._repository.create(data)
        
