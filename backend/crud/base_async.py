import logging
from typing import Any, Callable, List, Type, Optional, Union

from fastapi import Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import CRUDRouterBase, NOT_FOUND, _utils
from ._types import DEPENDENCIES, PAGINATION, PYDANTIC_SCHEMA as SCHEMA, SQLALCHEMY_MODEL as MODEL


class CRUDRouterAsync(CRUDRouterBase[SCHEMA]):
    def __init__(
        self,
        db: Any,
        db_model: Type[MODEL],
        schema: Type[SCHEMA],
        create_schema: Type[SCHEMA] = None,
        update_schema: Type[SCHEMA] = None,
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        paginate: Optional[int] = None,
        get_all_route: Union[bool, DEPENDENCIES] = True,
        get_one_route: Union[bool, DEPENDENCIES] = True,
        create_route: Union[bool, DEPENDENCIES] = True,
        update_route: Union[bool, DEPENDENCIES] = True,
        delete_one_route: Union[bool, DEPENDENCIES] = True,
        # delete_all_route: Union[bool, DEPENDENCIES] = True,
        **kwargs: Any
    ) -> None:

        self.db_model = db_model
        self.db_func = db
        self._pk: str = db_model.__table__.primary_key.columns.keys()[0]
        self._pk_type: type = _utils.get_pk_type(schema, self._pk)

        super().__init__(
            schema=schema,
            create_schema=create_schema,
            update_schema=update_schema,
            prefix=prefix or None,
            tags=tags,
            paginate=paginate,
            get_all_route=get_all_route,
            get_one_route=get_one_route,
            create_route=create_route,
            update_route=update_route,
            delete_one_route=delete_one_route,
            # delete_all_route=delete_all_route,
            **kwargs
        )

    def _get_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[MODEL]]:
        async def route(
            db: AsyncSession = Depends(self.db_func),  # type: ignore
            pagination: PAGINATION = self.pagination,
        ) -> List[MODEL]:
            skip, limit = pagination.get("skip"), pagination.get("limit")
            q = await db.execute(select(self.db_model).offset(skip).limit(limit))
            db_object = q.scalars().all()
            return db_object
        return route  # type: ignore

    def _get_one(self, *args: Any, **kwargs: Any) -> Callable[..., MODEL]:
        async def route(
            pk: self._pk_type, db: AsyncSession = Depends(self.db_func)  # type: ignore
        ) -> MODEL:
            db_object = await db.execute(select(self.db_model).where(self.db_model.id == pk))
            if db_object:
                return db_object.scalars().first()
            else:
                raise NOT_FOUND
        return route  # type: ignore

    def _create(self, *args: Any, **kwargs: Any) -> Callable[..., MODEL]:
        async def route(
            model: self.create_schema = Depends(self.create_schema),  # type: ignore
            db: AsyncSession = Depends(self.db_func),  # type: ignore
        ) -> MODEL:
            try:
                db_object = self.db_model(**model.dict(exclude_unset=True, exclude_none=True))  # type: ignore
                db.add(db_object)
                await db.commit()
                await db.refresh(db_object)
                return db_object
            except Exception as e:
                await db.rollback()
                logging.error(e.args)
                raise HTTPException(422, ", ".join(e.args))
        return route  # type: ignore

    def _update(self, *args: Any, **kwargs: Any) -> Callable[..., MODEL]:
        async def route(
            pk: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
            db: AsyncSession = Depends(self.db_func),  # type: ignore
        ) -> MODEL:
            try:
                db_object = await self._get_one()(pk, db)  # type: ignore
                for key, value in model.dict(exclude={self._pk}).items():
                    if hasattr(db_object, key):
                        setattr(db_object, key, value)
                await db.commit()
                await db.refresh(db_object)
                return db_object
            except Exception as e:
                await db.rollback()
                logging.error(e.args)
                raise HTTPException(422, ", ".join(e.args))
        return route  # type: ignore

    # def _delete_all(self, *args: Any, **kwargs: Any) -> Callable[..., List[MODEL]]:
    #     async def route(db: AsyncSession = Depends(self.db_func)) -> List[MODEL]:  # type: ignore
    #         try:
    #             await db.execute(delete(self.db_model))
    #             await db.commit()
    #             return await self._get_all()(db=db, pagination={"skip": 0, "limit": None})  # type: ignore
    #         except Exception as e:
    #             await db.rollback()
    #             logging.error(e.args)
    #             raise HTTPException(422, ", ".join(e.args))
    #     return route  # type: ignore

    def _delete_one(self, *args: Any, **kwargs: Any) -> Callable[..., MODEL]:
        async def route(
            pk: self._pk_type, db: AsyncSession = Depends(self.db_func)  # type: ignore
        ) -> MODEL:
            try:
                db_object = await self._get_one()(pk, db)  # type: ignore
                await db.delete(db_object)
                await db.commit()
                return db_object
            except Exception as e:
                await db.rollback()
                logging.error(e.args)
                raise HTTPException(422, ", ".join(e.args))
        return route  # type: ignore
