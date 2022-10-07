
import enum

from app.config import settings
from sqlalchemy import Column, Enum, Float, Integer, SmallInteger, String

from . import Base, Database

db = Database(settings.DATABASE_URL)


class UserRole(enum.Enum):
    admin_role = 'ADMIN_ROLE'
    user_role = 'USER_ROLE'


class ModelMixin:

    @classmethod
    def create(cls, **kw):
        return cls(**kw)

    def update(self, **kw):
        for attr, value in kw.items():
            setattr(self, attr, value)
        return self

class Product(Base, ModelMixin):

    __tablename__ = 'product'

    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True,
    )
    sku = Column(
        String(30),
        unique=True,
        nullable=False,
        info={
            'description': 'Unico identificador de producto'
        }
    )
    name = Column(
        String(80),
        nullable=False,
    )
    price = Column(
        Float(7,2),
        nullable=False,
        default='0,0'
    )
    brand = Column(
        String(20),
        nullable=False,
    )

class User(Base, ModelMixin):
    __tablename__ = 'user'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String(80),
        nullable=False,
    )
    email = Column(
        String(80),
        nullable=False,
    )
    password = Column(
        String(250),
        nullable=False,
    )
    state = Column(
        SmallInteger,
        default='1'
    )
    role = Column(
        Enum(UserRole),
        nullable=False,
    )
