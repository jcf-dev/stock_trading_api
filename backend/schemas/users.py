import datetime

from typing import Optional

from pydantic import BaseModel


class _UserBase(BaseModel):
    email: str
    username: str
    password: str
    updated: datetime.datetime
    created: datetime.datetime


class _UserDBBase(_UserBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class UserCreate(_UserBase):
    pass


class UserUpdate(_UserBase):
    pass


class User(_UserDBBase):
    pass
