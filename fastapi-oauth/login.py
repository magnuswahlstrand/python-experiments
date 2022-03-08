import os
from http.client import HTTPException

import httpx
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from encrypt import encrypt_message, decrypt_message

app = FastAPI()


@app.get("/login", response_class=HTMLResponse)
async def read_root():
    return f"""
<html>
  <body>
    <p>
      You are unauthenciated, please log in
    </p>
    <p>
        <a href="/auth/set_cookie">Log in</a>
    </p>
  </body>
</html>
    """


github_oauth_url = "https://github.com/login/oauth/access_token"
github_user_url = "https://api.github.com/user"

client_id = os.environ['GITHUB_CLIENT_ID']
client_secret = os.environ['GITHUB_CLIENT_SECRET']


@app.get("/callback")
async def read_item(code: str, response: Response):
    async with httpx.AsyncClient() as client:
        result = await client.post(github_oauth_url,
                                   json={
                                       'client_id': client_id,
                                       'client_secret': client_secret,
                                       'code': code
                                   },
                                   headers={'Accept': 'application/json'}
                                   )
        result.raise_for_status()

        # Validate token
        if 'access_token' not in result.json():
            raise HTTPException(status_code=500, detail="invalid request")
        access_token = result.json()['access_token']

        # Get user profile
        result = await client.get(github_user_url,
                                  headers={'Authorization': f'Token {access_token}'})
        result.raise_for_status()

        print(result.json())
        encrypted = encrypt_message({
            'auth_method': 'github',
            'display_name': result.json()['login'],
            'access_token': access_token
        })

        response.set_cookie(key="fastcodesession", value=encrypted)
        return result.json()


@app.get("/set_cookie")
async def set_cookie() -> RedirectResponse:
    response = RedirectResponse(url="/")

    message = {
        'id': 'a8098c1a-f86e-11da-bd1a-00112444be1e',
        'name': 'Magnus',
        'display_name': 'magnusw',
    }

    encoded_message = encrypt_message(message)
    print('SET COOKIE')
    print(decrypt_message(encoded_message))
    response.set_cookie(key="fastcodecookie", value=encoded_message)
    return response


@app.get("/remove_cookie")
async def remove_cookie() -> RedirectResponse:
    response = RedirectResponse(url="/")
    response.delete_cookie(key="fastcodecookie")
    return response
