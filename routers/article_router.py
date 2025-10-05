import json
import time
from fastapi import APIRouter
from starlette.responses import JSONResponse

from constants import ApiResponses
from dto.models import ArticleDTO
from rabbit_mq_wrapper import RabbitMQWrapper

api_router = APIRouter()
rabbit_mq_wrapper = RabbitMQWrapper()


@api_router.post("/articles")
def post_article(article: ArticleDTO):
    try:
        article = dict(article)
        article['timestamp'] = time.time()
        rabbit_mq_wrapper.publish_article(article)

        return JSONResponse(
            status_code=201,
            content={"message": ApiResponses.SUCCESS_MESSAGE.value}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": ApiResponses.INTERNAL_SERVER_ERROR.value}
        )
