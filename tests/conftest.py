import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from main import app
from models import Base
from config import DB_PORT_TEST, DB_HOST_TEST, DB_NAME_TEST,DB_PASS_TEST,DB_USER_TEST
from sqlalchemy.pool import NullPool



DATABASE_URL_TEST=f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

engine_test = create_async_engine(DATABASE_URL_TEST, echo=True,poolclass=NullPool)
test_async_session = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)
Base.metadata.bind=engine_test
async def override_get_async_session() -> AsyncGenerator[AsyncSession,None]:
    async with test_async_session() as session:
        yield session

app.dependency_overrides[get_db]=override_get_async_session

@pytest.fixture(autouse=True,scope="session")
async def test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient,None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client