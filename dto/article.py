from pydantic import BaseModel


class ArticleDTO(BaseModel):
    article: str
    date_uploaded: float
    owner_username: str
