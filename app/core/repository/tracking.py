
from abc import ABCMeta, abstractmethod

from app.core.schema.tracking import TrackingBase


class TrackingRepository(metaclass=ABCMeta):

    @abstractmethod
    def create(self, data: TrackingBase):
        raise NotImplementedError
