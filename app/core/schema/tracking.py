
from pydantic import BaseModel


class TrackingBase(BaseModel):
    entity: str
    data_id: str


class Tracking(TrackingBase):
    id: int
    class Config:
        orm_mode = True
