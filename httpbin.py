import traceback

from baize.asgi import request_response, Request, JSONResponse, PlainTextResponse
from baize.exceptions import HTTPException


@request_response
async def anything(request: Request) -> JSONResponse:
    try:
        try:
            form = list((await request.form).multi_items())
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
    except BaseException:
        return PlainTextResponse(traceback.format_exc(), 500)
