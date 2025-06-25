import aiohttp

UA = "Mozilla/5.0"


async def _fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, headers={"User-Agent": UA}, timeout=30) as rsp:
        rsp.raise_for_status()
        return await rsp.text()
