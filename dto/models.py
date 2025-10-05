from pydantic import BaseModel


class ArticleDTO(BaseModel):
    text: str
    date_uploaded: float
    username: str
