import uuid

from peewee import Model, CharField, PostgresqlDatabase, UUIDField, FloatField, ForeignKeyField
import bcrypt
import os

from dotenv import load_dotenv

load_dotenv()

db = PostgresqlDatabase(
    os.getenv('PSQL_DB'),
    user=os.getenv('PSQL_USER'),
    password=os.getenv('PSQL_PASS'),
    host=os.getenv('PSQL_HOST'),
    port=int(os.getenv('PSQL_PORT'))
)

db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    firstname = CharField()
    lastname = CharField()
    username = CharField()
    password_hash = CharField()

    class Meta:
        table_name = 'users'
        db = db

    def set_password(self, password: str):
        s = bcrypt.gensalt()

        self.password_hash = bcrypt.hashpw(password.encode(), s)

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password_hash)


class Article(BaseModel):
    class Meta:
        table_name = 'articles'

    owner_id = ForeignKeyField(User, on_delete='CASCADE', field=User.id, backref='articles')
    timestamp = FloatField()
    text = CharField()
    tag = CharField(null=True, default=None)
    id = UUIDField(primary_key=True, default=uuid.uuid4)
