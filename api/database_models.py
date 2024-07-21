import enum
import uuid

from sqlalchemy import Column, Enum, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    pass


class Status(enum.Enum):
    new = 'NEW'
    installing = 'INSTALLING'
    running = 'RUNNING'


class App(Model):
    __tablename__ = 'apps'

    UUID = Column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    kind = Column(String, nullable=False)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    description = Column(String, nullable=False)
    state = Column(Enum(Status), default=Status.new)
    json = Column(JSON)
