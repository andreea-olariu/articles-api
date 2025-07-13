from fastapi import FastAPI

from routers.article_router import api_router

app = FastAPI()
app.include_router(api_router)
