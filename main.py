import certifi
import sys
import os

import uvicorn
from curl_cffi import requests
from os.path import exists

from fastapi import FastAPI
from HttpRequest import HttpRequest
from HttpResponse import HttpResponse, HttpResponsePayload, HttpCookie

# noinspection PyBroadException
try:
    cert_path = certifi.where()
    print(cert_path)

    curl_cffi_cert = os.path.join(os.path.dirname(cert_path), "../curl_cffi/cacert.pem")
    print(curl_cffi_cert)
    if not exists(curl_cffi_cert):
        with open(cert_path, "rb") as src, open(curl_cffi_cert, "wb") as dst:
            dst.write(src.read())
except Exception:
    print("Certificate not found")
    quit()
app = FastAPI()


def get_http_only(cookie):
    extra_args = cookie.__dict__.get("_rest")
    if extra_args:
        for key in extra_args.keys():
            if key.lower() == "httponly":
                http_only = extra_args[key]
                if http_only:
                    return http_only
                return False
    return False


# noinspection PyBroadException
@app.post("/handle")
async def handle(r: HttpRequest):
    try:
        if r.method == "GET":
            r_method = requests.get
        elif r.method == "POST":
            r_method = requests.post
        elif r.method == "PUT":
            r_method = requests.put
        elif r.method == "PATCH":
            r_method = requests.patch
        elif r.method == "DELETE":
            r_method = requests.delete
        else:
            raise Exception(f"Method {r.method} is not supported")
        response = r_method(
            r.url,
            params=r.params,
            data=r.data,
            headers=r.headers,
            cookies=r.cookies,
            files=r.files,
            auth=r.auth,
            timeout=r.timeout,
            allow_redirects=r.allow_redirects,
            max_redirects=r.max_redirects,
            proxies=r.proxies,
            verify=r.verify,
            impersonate=r.impersonate,
        )

        cookies = [
            HttpCookie(
                name=k.name,
                value=k.value,
                path=k.path,
                domain=k.domain,
                secure=k.secure,
                http_only=get_http_only(k),
            )
            for k in list(response.cookies.jar)
        ]

        return HttpResponse(
            success=True,
            error=None,
            payload=HttpResponsePayload(
                url=r.url,
                status=response.status_code,
                content=response.text,
                headers=response.headers,
                cookies=cookies,
            ),
        )
    except Exception as e:
        return HttpResponse(success=False, error=str(e))


def get_args(name="default", host="127.0.0.1", port=1337):
    return host, int(port)


if __name__ == "__main__":
    host, port = get_args(*sys.argv)
    uvicorn.run(app, host=host, port=port)
