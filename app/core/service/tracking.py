
from app.core.repository.tracking import TrackingRepository


class TrackingService:

    def __init__(self, tracking_repository: TrackingRepository):
        self._tracking_repository = tracking_repository

    def create(self, data):
        return self._tracking_repository.create(data)
        
