from typing import Dict, TypeVar, Optional, Sequence

from fastapi.params import Depends
from pydantic import BaseModel

from ..db.base import Base

PAGINATION = Dict[str, Optional[int]]
PYDANTIC_SCHEMA = BaseModel
SQLALCHEMY_MODEL = Base

BASE_SCHEMA = TypeVar('BASE_SCHEMA', bound=BaseModel)
BASE_MODEL = TypeVar('BASE_MODEL', bound=Base)

DEPENDENCIES = Optional[Sequence[Depends]]
