import aiohttp
import structlog

logger = structlog.get_logger(__name__)


async def fetch_data(session: aiohttp.ClientSession, url: str) -> list[dict]:
    """Fetch block data."""
    try:
        async with session.get(url, timeout=20) as resp:
            resp.raise_for_status()
            payload = await resp.json()
            return payload.get("items", [])
    except Exception as e:
        logger.exception("Fetch error", url=url, error=e)
        return []
