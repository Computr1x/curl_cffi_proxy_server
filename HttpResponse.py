from typing import Optional, List
from pydantic import BaseModel


class HttpCookie(BaseModel):
    name: str
    value: str
    path: str
    domain: str
    secure: bool
    http_only: bool


class HttpResponsePayload(BaseModel):
    url: str
    status: int
    content: str
    cookies: List[HttpCookie]
    headers: dict

    class Config:
        arbitrary_types_allowed = True


class HttpResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    payload: Optional[HttpResponsePayload] = None,

    class Config:
        arbitrary_types_allowed = True
