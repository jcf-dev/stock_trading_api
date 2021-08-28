from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Date, ForeignKey, TIMESTAMP, Integer, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..db.base_class import Base


if TYPE_CHECKING:
    from .traders import Trader  # noqa: F401


class User(Base):
    email = Column(String(64), unique=True)
    username = Column(String(10), unique=True)
    password = Column(String(128))
    updated = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # FK Reverse Relations (`uselist` tells the SQLAlchemy that this is a one-to-one relationship)
    trader = relationship('Trader', backref='user', uselist=False)

    def __repr__(self):
        return f"<User(username='{self.username}')>"
