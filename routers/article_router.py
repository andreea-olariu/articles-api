import time

from fastapi import APIRouter
from starlette.responses import JSONResponse

from constants import ApiResponses
from db.models import Article, User
from dto.article import ArticleDTO
from rabbit_mq_wrapper import RabbitMQWrapper

api_router = APIRouter()
rabbit_mq_wrapper = RabbitMQWrapper()


@api_router.post("/articles")
def post_article(article: ArticleDTO):
    try:
        article_document = Article(text=article.article, timestamp=time.time(),
                                   owner_id=User.get(User.username == article.owner_username))

        saved = article_document.save(force_insert=True)

        if saved:
            article = article.model_dump(mode="json")
            article['id'] = str(article_document.id)
            rabbit_mq_wrapper.publish_article(article)

            return JSONResponse(
                content={"message": ApiResponses.SUCCESS_MESSAGE.value},
                status_code=201
            )

        else:
            return JSONResponse(
                content={"message": ApiResponses.FAILED_TO_INSERT.value},
                status_code=500
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": ApiResponses.INTERNAL_SERVER_ERROR.value}
        )
