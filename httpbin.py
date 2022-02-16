import traceback
from typing import Awaitable, Callable

from baize.asgi import request_response, middleware, Request, Response, JSONResponse, PlainTextResponse
from baize.datastructures import UploadFile
from baize.exceptions import HTTPException


@middleware
async def catch_exception(request: Request, next_call: Callable[[Request], Awaitable[Response]]) -> Response:
    try:
        response = await next_call(request)
    except BaseException:
        return PlainTextResponse(traceback.format_exc(), 500)


@request_response
@catch_exception
async def anything(request: Request) -> JSONResponse:
    try:
        form = [
            (
                name,
                value if isinstance(value, str) else
                {"filename": value.filename, "content-type": value.content_type}
            )
            for name, value in (await request.form).multi_items()
        ]
    except HTTPException:
        form = {}

    try:
        json = await request.json
    except HTTPException:
        json = {}

    try:
        if not (form or json):
            content = (await request.body).decode()
        else:
            content = ""
    except UnicodeDecodeError:
        content = ""

    return JSONResponse(
        {
            "method": request.method,
            "urlpath": request.url.path,
            "query_params": list(request.query_params.multi_items()),
            "headers": dict(request.headers),
            "cookies": request.cookies,
            "form": form,
            "json": json,
            "content": content,
        }
    )
