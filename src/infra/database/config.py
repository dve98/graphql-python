from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from sqlmodel import SQLModel
import os

# Load variables from .env file


DB_CONFIG = os.environ['DB_CONFIG']
class DatabaseSession:
    def __init__(self, url: str = DB_CONFIG):
        self.engine = create_async_engine(url)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    # close connection
    async def close(self):
        await self.engine.dispose()

    # Prepare the context for the asynchronous operation
    async def __aenter__(self) -> AsyncSession:
        self.session = self.SessionLocal()
        return self.session

    # it is used to clean up resources,etc.
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_db(self) -> AsyncSession:
        async with self as db:
            yield db

    async def commit_rollback(self):
        try:
            await self.session.commit() 
        except Exception:
            await self.session.rollback()
            raise


db = DatabaseSession()