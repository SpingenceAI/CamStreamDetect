"""VLM Demo App"""
import os
from loguru import logger
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes import router

def app_factory():
    """Create a FastAPI app."""
    app = FastAPI()
    app.include_router(router)
    #mount the frontend (index.html) to the root path
    app.mount("/UI", StaticFiles(directory="build", html=True), name="fe")
    app.mount("/static", StaticFiles(directory="build/static"), name="static")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

def init_logger(log_path):
    """init logger"""
    logger_folder = os.path.split(log_path)[0]
    os.makedirs(logger_folder, exist_ok=True)
    logger.add(
        log_path, rotation="00:00", encoding="utf-8", enqueue=True, retention="10 days"
    )
    logger.info("INIT LOGGER")

if __name__ == "__main__":
    init_logger("./log/demo_log.log")

    app = app_factory()
    uvicorn.run(app, host="0.0.0.0", port=7860)