from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
from app.config import settings
from app.database import engine, Base
# Import models to register them with Base
from app.routers import auth , users , transactions , categories

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and httpx client
    print("Starting up...")
    Base.metadata.create_all(bind=engine)
    app.state.http_client = httpx.AsyncClient()
    
    yield
    
    # Shutdown: Close httpx client
    print("Shutting down...")
    await app.state.http_client.aclose()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)

# Include routers here later
# app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(auth.router , prefix=f"{settings.api_v1_str}/auth", tags=["Authentication"] )
app.include_router(users.users_router , prefix=f"{settings.api_v1_str}/users", tags=["Users"] )
app.include_router(transactions.router , prefix=f"{settings.api_v1_str}", tags=["Transactions"] )
app.include_router(categories.router , prefix=f"{settings.api_v1_str}", tags=["Categories"] )


@app.get("/")
async def read_root():
    return {
        "message": "Welcome To The Personal Finance Tracker API",
        "docs": "/docs",
        "version": "v1"
    }

@app.get("/health")
async def check_health():
    return {"status": "healthy"}