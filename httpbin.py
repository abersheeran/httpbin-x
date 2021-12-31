from baize.asgi import request_response, Request, JSONResponse
from baize.exceptions import HTTPException


@request_response
async def anything(request: Request) -> JSONResponse:
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
            "headers": dict(request.headers),
            "form": form,
            "json": json,
            "content": content,
        }
    )
