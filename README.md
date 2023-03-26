# curl_cffi_proxy_server
Simple proxy server based on https://github.com/yifeikong/curl_cffi


# Install
```commandline
pip install -r /path/to/requirements.txt
```

# Build to exe
```commandline
pip install pyinstaller

pyinstaller .\main.py --hidden-import=_cffi_backend --collect-all curl_cffi --paths=.\venv\Lib\site-packages --noconfirm
```

# Run
```commandline
python main.py [host] [port]
```

# Main structures

##  [HttpRequest](https://github.com/Computr1x/curl_cffi_proxy_server/blob/master/HttpRequest.py)
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

##  [HttpResponse](https://github.com/Computr1x/curl_cffi_proxy_server/blob/master/HttpResponse.py)
    success: bool
    error: Optional[str] = None
    payload: Optional[HttpResponsePayload] = None,

##  [HttpResponsePayload](https://github.com/Computr1x/curl_cffi_proxy_server/blob/master/HttpResponse.py)
    url: str
    status: int
    content: str
    cookies: List[HttpCookie]
    headers: dict