import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app

pytestmark = pytest.mark.asyncio

@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture
def transport():
    return ASGITransport(app=app)

@pytest.mark.anyio
async def test_root_redirect(transport):
    # Arrange
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Act
        response = await ac.get("/")
    # Assert
    assert response.status_code in (200, 307, 302)

@pytest.mark.anyio
async def test_list_activities(transport):
    # Arrange
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

@pytest.mark.anyio
async def test_signup_activity(transport):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    url = f"/activities/{activity}/signup"
    params = {"email": email}
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Act
        response = await ac.post(url, params=params)
    # Assert
    assert response.status_code in (200, 400)
