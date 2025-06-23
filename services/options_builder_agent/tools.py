import httpx
from langchain.tools import tool
from .config import BASE_URL, ENDPOINTS

client = httpx.AsyncClient(base_url=BASE_URL, timeout=10.0)

@tool
async def flight_options(flight_ctx: dict) -> list:
    """GET alternate flights."""
    r = await client.post(ENDPOINTS["flight_options"], json={"flight_ctx": flight_ctx})
    r.raise_for_status()
    return r.json()

@tool
async def hotel_options(flight_ctx: dict) -> list:
    """GET available hotels."""
    r = await client.post(ENDPOINTS["hotel_options"], json={"flight_ctx": flight_ctx})
    r.raise_for_status()
    return r.json()

@tool
async def lounge_options(flight_ctx: dict) -> list:
    """GET available lounges."""
    r = await client.post(ENDPOINTS["lounge_options"], json={"flight_ctx": flight_ctx})
    r.raise_for_status()
    return r.json()
