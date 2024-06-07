from fastapi import FastAPI, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.auth import get_current_user, oauth2_scheme, SECRET_KEY, ALGORITHM

async def auth_middleware(request: Request, call_next):
    if request.url.path in ["/token", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    try:
        token = request.headers.get("Authorization").split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except (JWTError, IndexError):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    return await call_next(request)

def setup_middleware(app: FastAPI):
    app.middleware("http")(auth_middleware)
