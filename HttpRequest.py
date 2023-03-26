from typing import Union, Dict, Optional, Tuple

from curl_cffi.requests import HeaderTypes, CookieTypes, BrowserType
from pydantic import BaseModel, validator


class HttpRequest(BaseModel):
    method: str
    url: str
    params: dict = None
    data: Union[Dict[str, str], str, bytes] = None
    headers: HeaderTypes = None
    cookies: CookieTypes = None
    files: Dict = None
    auth: Tuple[str, str] = None
    timeout: Union[float] = 30
    allow_redirects: bool = True
    max_redirects: Union[int, None] = 3
    proxies: dict = None
    verify: bool = None
    impersonate: Union[str] = None

    @validator('params')
    def set_params(cls, params):
        return params or None

    class Config:
        arbitrary_types_allowed = True

