from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
import logging
from app.auth import authenticate_user, create_access_token, get_current_active_user, User, Token
from app.routers import endpoints, conversations
from app.middleware import setup_middleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "human@example.com": {
        "username": "human",
        "full_name": "Human Being",
        "email": "human@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$Ls9jNx/L/63Ph/ZsRh8kDQ$rl8obcNCnHXYfnnOubXJ/Rw4o8dEC7chzWaZIpYMgQI",  # Correctly hashed password
        "disabled": False,
    }
}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

Instrumentator().instrument(app).expose(app)

app.include_router(endpoints.router)
app.include_router(conversations.router)

setup_middleware(app)
