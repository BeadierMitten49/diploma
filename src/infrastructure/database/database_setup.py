import os

from sqlalchemy import create_engine
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.utils.pascal_to_snake_case import pascal_to_snake_case


DATABASE_URL = os.getenv("DATABASE_URL")
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


@as_declarative()
class BaseOrm:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return pascal_to_snake_case(cls.__name__).replace("_orm", "")


engine = create_engine(DATABASE_URL)
async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def init_db():
    BaseOrm.metadata.create_all(engine)


class Storage:
    def __init__(self, session: async_sessionmaker = async_session):
        self.session = session
