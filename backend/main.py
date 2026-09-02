from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, auth, portfolio, mails
from app.core.config import settings

app = FastAPI(title="Cold Email Generator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
app.include_router(mails.router, prefix="/mails", tags=["mails"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
