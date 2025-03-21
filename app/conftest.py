import pytest_asyncio
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """
    Async client fixture for testing API endpoints.
    """
    async with AsyncClient(transport=app, base_url="http://test") as client:
        yield client


# Use pytest-asyncio's built-in event_loop fixture instead
# of defining our own to avoid warnings
