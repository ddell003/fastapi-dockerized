from typing import List

from fastapi import Query


class BaseQueryParams:
    def __init__(
        self,
        q: str = Query(None),
        limit: int = Query(None),
        offset: int = Query(None),
        sort: str = Query(None),
        direction: str = Query(
            "desc", regex="(?:[\\s]|^)(asc|desc)(?=[\\s]|$)"
        ),  # noqa:W605
    ):
        self.q = q
        self.limit = limit
        self.offset = offset
        self.sort = sort
        self.direction = direction


class UserQueryParams(BaseQueryParams):
    def __init__(
        self,
        q: str = Query(None),
        limit: int = Query(None),
        offset: int = Query(None),
        sort: str = Query(None),
        direction: str = Query(
            "desc", regex="(?:[\\s]|^)(asc|desc)(?=[\\s]|$)"
        ),  # noqa:W605
        email: List[str] = Query(
            None, example={"email=email1@gmail.com", "email=email2@gmail.com"}
        ),
        roles: List[int] = Query(None, example={"role=1", "role=2"}),
        active: bool = Query(None, example={"active=True"}),
    ):
        self.email = email
        self.roles = roles
        self.active = active

        super(UserQueryParams, self).__init__(q, limit, offset, sort, direction)
