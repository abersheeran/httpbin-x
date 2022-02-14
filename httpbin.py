import traceback

from baize.asgi import request_response, Request, JSONResponse, PlainTextResponse
from baize.exceptions import HTTPException


@request_response
async def anything(request: Request) -> JSONResponse:
    try:
        form = list((await request.form).multi_items())
    except HTTPException:
        form = {}
    except BaseException:
        return PlainTextResponse(traceback.format_exc(), 500)

    try:
        json = await request.json
    except HTTPException:
        json = {}
    except BaseException:
        return PlainTextResponse(traceback.format_exc(), 500)

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
