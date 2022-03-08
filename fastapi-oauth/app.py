from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse

from encrypt import decrypt_message

app = FastAPI()


@app.middleware("http")
async def check_cookie(request: Request, call_next):
    if 'fastcodecookie' not in request.cookies:
        print('cookie is NOT set')
        return RedirectResponse(url='/auth/login')

    print('cookie is set')
    user = decrypt_message(request.cookies['fastcodecookie'])
    print(f'welcome', user)

    request.state.user = user
    return await call_next(request)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return f"""
<html>
  <body>
    <p>
      Well, hello there! You are logged in as {request.state.user['display_name']}!
    </p>
    <p>
        <a href="/auth/remove_cookie">Logout</a>
    </p>
  </body>
</html>
    """
