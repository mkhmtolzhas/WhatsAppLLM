from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.global_router import router
from .listeners import Listener

class AppCreator:
    def __init__(self, allow_origins: list[str] = ["*"]):
        self.app = FastAPI(
            title="LLM for WhatsAppBot",
            description="LLM for WhatsAppBot",
            version="0.1.0",
        )
        self.setup_middlewares(allow_origins)
        self.setup_routers()
        self.setup_listeners()


    def setup_middlewares(self, allow_origins: list[str]):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routers(self):
        self.app.include_router(router)
    
    def setup_listeners(self):
        Listener.init_listeners(self.app)
        

    def get_app(self) -> FastAPI:
        return self.app
    

app_creator = AppCreator()