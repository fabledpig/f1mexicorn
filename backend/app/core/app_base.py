from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api_router import api_router

allowed_origins = ["*"]


class Application(FastAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.include_router(api_router)

    def add_middlewares(self):
        pass

    def add_event_handlers(self):
        pass
