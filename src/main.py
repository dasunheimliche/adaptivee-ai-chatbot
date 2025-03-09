import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

import uvicorn

from src.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def healthcheck():
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "debug_mode": settings.DEBUG,
        "avaliable_ai_providers": settings.AVAILABLE_AI_PROVIDERS,
    },

if __name__ == "__main__":
    logging.info(f"Starting {settings.APP_NAME} en modo debug={settings.DEBUG}")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)