from fastapi import FastAPI
from app.api.v1.api_router import api_router

class Application(FastAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.include_router(api_router)

    def add_middlewares(self):
        pass

    def add_event_handlers(self):
        pass
